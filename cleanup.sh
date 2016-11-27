#!/usr/bin/env bash

find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete
export DATABASE_URL="postgresql://localhost/app"
export SECRET_KEY="a4b814b8)1ecafedbRuU8fX719'ae7fob13"
export FLASK_COVERAGE="1"
export CSRF_SESSION_KEY="dfgbodbfa63r3ohnafd0apthn4"
