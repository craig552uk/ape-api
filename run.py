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
    from faker import Factory
    fake = Factory.create()

    for _ in range(0,3):
        account = Account(name=fake.company())
        db.session.add(account)
    
        for _ in range(0,3):
            account.users.append(User(name=fake.name()))

        for _ in range(0,3):
            account.visitors.append(Visitor())
            
        for name in ["Mobile Users", "Recent Visitors", "Repeat Customers"]:
            segment = Segment(name=name)
            account.segments.append(segment)

            for field in ["url", "domain", "referral"]:
                segment.rules.append(Rule(group_id=0, field=field, comparator="EQUAL", value="FooBar"))

        for name in ["Account Page LH Sidebar", "Home Page Banner", "Product Page RH Sidebar"]:
            placeholder = Placeholder(name=name)
            account.placeholders.append(placeholder)

            for name in ["City Break Banner", "Family Fun Banner", "Winter Sun Banner"]:
                placeholder.components.append(Component(name=name))

    db.drop_all()
    db.create_all()
    db.session.commit()


def db_show():
    """Display data in the DB"""
    for account     in Account.query.all():     print account
    for user        in User.query.all():        print user
    for visitor     in Visitor.query.all():     print visitor
    for placeholder in Placeholder.query.all(): print placeholder
    for component   in Component.query.all():   print component
    for segment     in Segment.query.all():     print segment
    for rule        in Rule.query.all():        print rule


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

    run_app = True

    if args.db_rebuild:
        run_app = False
        db.drop_all()
        db.create_all()

    if args.db_seed:
        run_app = False
        db_seed()

    if args.db_show:
        run_app = False
        db_show()

    if args.cli:
        import pdb
        run_app = False
        print CLI_MESSAGE
        pdb.set_trace()

    if run_app:
        app.run(host=args.host, port=args.port)