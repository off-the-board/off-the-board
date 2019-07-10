import sys
import unittest

import coverage
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

cov = coverage.coverage(
    branch=True,
    include="project/*",
    omit=[
        "project/tests/*",
        "project/config.py",
    ]
)
cov.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)
    

@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    db.session.add(User(username="dgood", email="danielgoodman@gmail.com"))
    db.session.add(User(username="cking", email="cking@gmail.com"))
    db.session.commit()


@cli.command("check_coverage")
def check_coverage():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        cov.stop()
        cov.save()
        print("Coverage Summary:")
        cov.report()
        cov.html_report()
        cov.erase()
        return 0
    sys.exit(result)


if __name__ == "__main__":
    cli()
