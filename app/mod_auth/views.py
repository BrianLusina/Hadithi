from . import auth
from flask import render_template, request, flash, redirect, url_for, session
from .forms import LoginForm, RegisterForm, ForgotPassword
from .models import AuthorAccount, AsyncOperationStatus, AsyncOperation
from app import db
from flask_login import logout_user, login_required, login_user, current_user
from app.mod_auth.token import generate_confirmation_token, confirm_token
from datetime import datetime
from app.mod_auth.email import send_mail
from app.mod_auth.facebook_auth import FacebookSignIn
from app.utils.taskmanager import taskman
from app.mod_auth.controllers import facebook_external_auth


@auth.route('/login', methods=["POST", "GET"])
def login():
    """
    Login route for user's to login to their accounts
    :return: Login view
    """
    login_form = LoginForm(request.form, prefix="login-form")
    if request.method == "POST":
        if login_form.validate_on_submit():
            author = AuthorAccount.query.filter_by(email=login_form.email.data).first()

            if author is not None and author.verify_password(login_form.password.data):
                # login the user
                login_user(author, login_form.remember_me.data)

                flash(message="Welcome back {}!".format(author.username), category="success")

                return redirect(url_for('dashboard.user_dashboard', username=author.username))
            flash(message="Invalid email and/or password", category="error")
    return render_template('auth.login.html', login_form=login_form, user=current_user)


@auth.route('/register', methods=["POST", "GET"])
def register():
    """
    Processes the registration form details. This is used to add the user to the database, if they
    are not there, redirects them to their dashboard when registration is complete

    Sends and email verification to user based on the email provided.
    :return the register form
    """
    register_form = RegisterForm(request.form, prefix="register-form")
    if request.method == "POST":
        if register_form.validate_on_submit():

            # check if the email already exists
            author_email = AuthorAccount.query.filter_by(email=register_form.email.data).first()
            author_username = AuthorAccount.query.filter_by(username=register_form.username.data).first()

            # if no author exists with such an email or username, then register them
            if author_email is None and author_username is None:
                author_email = AuthorAccount(first_name=register_form.first_name.data,
                                             last_name=register_form.last_name.data,
                                             username=register_form.username.data,
                                             email=register_form.email.data,
                                             password=register_form.password.data,
                                             confirmed=False,
                                             registered_on=datetime.now())

                db.session.add(author_email)
                # make the user follow themselves
                db.session.add(author_email.follow(author_email))
                db.session.commit()

                # generate token for email verification
                token = generate_confirmation_token(author_email.email)

                # _external adds the full absolute URL that includes the hostname and port
                confirm_url = url_for('auth.confirm_email', token=token, _external=True)

                # build the message
                html = render_template('auth.confirm_email.html', confirm_url=confirm_url,
                                       user=current_user)
                subject = "Please confirm your email"

                # send the user an email
                send_mail(author_email.email, subject, html)

                # login the user
                login_user(author_email)
                flash(message='A confirmation email has been sent via email.', category='success')

            else:
                # display the appropriate error message based on what is a duplicate
                if author_email is not None:
                    register_form.email.errors.append("Email already registered")
                    flash(message="Email already registered", category="error")
                if author_username is not None:
                    register_form.email.errors.append("Username already registered")
                    flash(message="Username already registered", category="error")

            # redirect the unconfirmed users to their dashboard, but to the unconfirmed view
            return redirect(url_for('dashboard.unconfirmed'))
    return render_template('auth.register.html', register_form=register_form, user=current_user)


@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    """
    Confirm email route for the user. Checks if the author has already confirmed their account
    If they have, log them in. If they have not, confirm their account and direct them to their dashboard
    we call the confirm_token() function, passing in the token. If successful, we update the user,
    changing the email_confirmed attribute to True and setting the datetime for when the confirmation took place.
    Also, in case the user already went through the confirmation process – and is confirmed –
    then we alert the user of this.

    :param token: Generated in the user registration
    :return: A redirect to login
    """

    # if the current user had been confirmed, redirect them to login
    if current_user.confirmed:
        flash(message='Account already confirmed. Please login.', category='success')
        return redirect(url_for('auth.login'))

    # else confirm them
    # get the email for the confirmed

    email = confirm_token(token)

    # get the author or throw an error
    author = AuthorAccount.query.filter_by(email=current_user.email).first_or_404()

    if author.email == email:
        author.confirmed = True
        author.confirmed_on = datetime.now()

        # update the confirmed_on column
        db.session.add(author)
        db.session.commit()
        flash(message='You have confirmed your account. Thanks!', category='success')

        # redirect to login
        return redirect(url_for('auth.login'))
    else:
        flash(message='The confirmation link is invalid or has expired.', category='danger')
    # redirect to the user's dashboard
    return redirect(url_for('auth.login'))


@auth.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    forgot_pass = ForgotPassword(request.form)
    return render_template('auth.password-recovery.html', forgot_pass=forgot_pass, user=current_user)


@auth.route("/facebook_authorize")
def facebook_authorize():
    """
    This starts the authorization process with facebook
    :return:
    """
    # if the user is logged in already, redirect them to dashboard
    if not current_user.is_anonymous:
        return redirect(url_for("dashboard.user_dashboard", username=current_user.username))
    # if user is anonymous, begin the sign in process
    oauth = FacebookSignIn()
    return oauth.authorize()


# todo google auth
@auth.route("/google_authorize")
def google_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for("dashboard.user_dashboard", username=current_user.username))


# todo twitter auth
@auth.route("/twitter_authorize")
def twitter_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for("dashboard.user_dashboard", username=current_user.username))


@auth.route("/callback")
def show_preloader_start_auth():
    """
    Send user to the page with a preloader
    Start background communication with Facebook
    Because communication with other services via http is usually long,
    that’s way is performed in a separate thread.
    This forces us to place the code where our application talks to Facebook in a different task.
    The user, during this process, sees the preloader page and must wait until the background thread finishes

    This will create the record of the async_operation, that represents the status of task execution:
     pending, ok, error. We’ll also store the id of the async_operation within the session.
     Based on this value, we can retrieve the appropriate record of the async_operation when it’s time
     to change its status.
    :return: redirect url for the preloader

    """
    if not current_user.is_anonymous:
        return redirect(url_for("dashboard.user_dashboard", username=current_user.username))

    # store in the session id of the asynchronous operation
    status_pending = AsyncOperationStatus.query.filter_by(code="pending").first()

    if status_pending is None:
        status_pending = AsyncOperation(code="pending")
        db.session.add(status_pending)
        db.session.commit()

        async_operation = AsyncOperation(async_operation_status_id=status_pending.id)
        db.session.add(async_operation)
        db.session.commit()

        # store in a session the id of Asynchronous Operation
        session["async_operation_id"] = str(async_operation.id)

    # run external auth in a separate thread
    taskman.add_task(facebook_external_auth)
    return redirect(url_for("auth.preloader"))


@auth.route("/get-status")
def get_status():
    """
    checks to see if the status of the async_operation is set to ‘ok’.
    handles this and retrieves the status of the current async_operation.
    :return:
    """
    if "async_operation_id" in session:
        async_operation_id = session["async_operation_id"]

        # retrieve from the db the status of the store session async operation
        async_operation = AsyncOperation.query.filter_by(id=async_operation_id).join(AsyncOperationStatus).first()

        status = str(async_operation.status.code)
        print(status)
    else:
        print("async operation not in session")
        return redirect(url_for(error))
    return status


# renders a loader page
@auth.route('/preloader')
def preloader():
    return render_template('auth.preloader.html')


# renders an error page
@auth.route('/error')
def error():
    return render_template('auth.error.html')


@auth.route("/success")
def success():
    """
    Success route which will be accessed when the user successfully logs in with Facebook.
    JavaScript will handle the routing to this function
    :return: redirect to user dashboard on successful login
    """
    if "async_operation_id" in session:
        async_operation_id = session["async_operation_id"]
        async_operation = AsyncOperation.query.filter_by(id=async_operation_id).first()
        author = AuthorAccount.query.filter_by(id=async_operation.author_profile_id).first()
        login_user(author, True)
    return redirect(url_for("dashboard.user_dashboard", user_name=current_user.username))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))
