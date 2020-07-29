from flask.cli import FlaskGroup

from project import app, db, User


cli = FlaskGroup(app)


# cli allows to use flask functions from cmd
# like this: python manage.py do_fun
@cli.command("do_fun")
def do_fun():
    """Do fun!"""
    print("You spin me right round, baby".center(70, " "))
    print("Right round like a record, baby".center(70, " "))
    print("Right round round round".center(70, " "))


@cli.command("create_db")
def create_db():
    """Create database."""
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Don't use it, just an example of add()."""
    db.session.add(User(email="test.user@email.com"))
    db.session.commit()


if __name__ == "__main__":
    cli()
