# Hadithi

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0ec18362f0ab4e7486c01559f329f2a2)](https://www.codacy.com/app/BrianLusina/Hadithi?utm_source=github.com&utm_medium=referral&utm_content=BrianLusina/Hadithi&utm_campaign=badger)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/0ec18362f0ab4e7486c01559f329f2a2)](https://www.codacy.com/app/BrianLusina/Hadithi?utm_source=github.com&utm_medium=referral&utm_content=BrianLusina/Hadithi&utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.org/BrianLusina/Hadithi.svg?branch=master)](https://travis-ci.org/BrianLusina/Hadithi)
[![CircleCI](https://circleci.com/gh/BrianLusina/Hadithi.svg?style=svg)](https://circleci.com/gh/BrianLusina/Hadithi)
[![codecov](https://codecov.io/gh/BrianLusina/Hadithi/branch/master/graph/badge.svg)](https://codecov.io/gh/BrianLusina/Hadithi)

This is a website featuring some of Africa's best short stories titled Hadithi. The site has a sample of 10 short stories and allows the user the ability to share each story on social media. Even make a comment on each story.

Technologies used:
+ flask python framework
+ HTML/CSS
+ JavaScript jQuery library

## setup with Heroku
Run this in terminal:

``` sh
$ heroku addons:add heroku-postgresql:hobby-dev
```

Setup DATABASE_URL variable

``` sh
$ heroku pg:promote HEROKU_POSTGRESQL_<COLOR>_URL
```

Initialize the database locally

``` sh
$ python manage.py init_app
```
> this will initialize the application's db with Postgres

Initialize the db on Heroku

``` sh
$ heroku run python manage.py init_app
```
> creates an initial db on Heroku

