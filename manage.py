import os
from app import create_app
# , db
# from app.models import ChamaGroup, User, AccountActivity, Calender, ChamaProjects, Milestones
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate

cov = None
if os.environ.get("FLASK_COVERAGE"):
    from coverage import coverage
    cov = coverage(branch=True, include='app/')
    cov.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# migrate = Migrate(app, db)


# def make_shell_context():
#     return dict(app=app, db=db, Chamagroup=ChamaGroup, User=User, AccountActivity=AccountActivity,
#                 Calender=Calender, ChamaProjects=ChamaProjects, Milestones=Milestones)
#
#
# manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage_var=False):
    """
    Run unit tests and print out coverage report
    :param coverage_var:
    :return:
    """
    if coverage_var and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'coverage')
        cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()


@manager.command
def init_app():
    """
    Run database initialization
    :return:
    """
    from flask_migrate import init, migrate, upgrade

    # initialize migrations
    migrations_dir = os.path.join(app.config['ROOT_DIR'], 'migrations')
    if not os.path.exists(migrations_dir):
        init()

    # perform database migrations
    migrate()

    # migrate database to latest revision
    upgrade()

    print("Migrations completed" + "." * 10)
    # initialize database with default records
    # from app.utils.init_db import InitializeDatabase
    # init_db = InitializeDatabase()
    #
    # init_db.add_chama_group()
    # init_db.add_user_accounts()
    # init_db.add_chama_projects()

    print("Database records added" + "." * 10)


if __name__ == '__main__':
    manager.run()
