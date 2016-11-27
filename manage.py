import os
cov = None
if os.environ.get("FLASK_COVERAGE"):
    from coverage import coverage
    cov = coverage(branch=True, include='app/')
    cov.start()

