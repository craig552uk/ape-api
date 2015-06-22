# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# Application entry-point and utility methods

import os, sys, argparse

CLI_MESSAGE = """Flask Application CLI Debugger
Useful Methods:
  db.drop_all()   # Drop all tables in DB
  db.create_all() # Create all tables in DB
  db_seed()       # Populate DB with sample data
  db_show()       # View objects in DB
Objects in scope:
  app             # The Flask Application
  db              # The SQLAlchemy DB
"""

## Helpful methods ##

def db_seed():
    """Rebuild the database populating it with seed data"""
    db.drop_all()
    db.create_all()
    db.session.add(User(name="Craig"))
    db.session.add(User(name="Vicky"))
    db.session.add(User(name="Sophie"))
    db.session.add(Customer(name="Google"))
    db.session.add(Customer(name="Apple"))
    db.session.add(Customer(name="Amazon"))
    db.session.add(Visitor())
    db.session.add(Visitor())
    db.session.add(Visitor())
    db.session.add(Placeholder(name="Home Page Banner"))
    db.session.add(Placeholder(name="Product Page RH Sidebar"))
    db.session.add(Placeholder(name="Account Page LH Sidebar"))
    db.session.add(Component(name="Winter Sun Banner"))
    db.session.add(Component(name="Family Fun Banner"))
    db.session.add(Component(name="City Break Banner"))
    db.session.commit()


def db_show():
    """Display data in the DB"""
    for user        in User.query.all():        print user
    for customer    in Customer.query.all():    print customer
    for visitor     in Visitor.query.all():     print visitor
    for placeholder in Placeholder.query.all(): print placeholder
    for component   in Component.query.all():   print component


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--host',       default='0.0.0.0',      help="Server host")
    parser.add_argument('--port',       default=8000, type=int, help="Server port")
    parser.add_argument('--config-file',                        help="Absolute path to configuration file")
    parser.add_argument('--db-rebuild', action='store_true',    help="Rebuild DB")
    parser.add_argument('--db-seed',    action='store_true',    help="Rebuild & populate DB")
    parser.add_argument('--db-show',    action='store_true',    help="Show data in the DB")
    parser.add_argument('--cli',        action='store_true',    help="Run with CLI")
    args = parser.parse_args()

    # Set config file if provided
    if args.config_file:
        os.environ['FLASK_APP_CONFIG'] = args.config_file

    # app import after config file definition
    from app import app, db
    from app.routes import *
    from app.models import *

    if args.db_rebuild:
        db.drop_all()
        db.create_all()

    elif args.db_seed:
        db_seed()

    elif args.db_show:
        db_show()

    elif args.cli:
        import pdb
        print CLI_MESSAGE
        pdb.set_trace()

    else:
        app.run(host=args.host, port=args.port)