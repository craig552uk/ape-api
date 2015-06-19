Install
=======

Set up environment with:

    > virtualenv venv
    > . venv/bin/activate
    > pip install -r requirements.txt

Run application:

    > python run.py

Build database with:

    > python run.py --db-rebuild

Populate DB with seed data:

    > python run.py --db-seed

Show contents of DB:

    > python run.py --db-show

Run application with specified host:port
    
    > python run.py --host 0.0.0.0 --port 8080

Run application with custom config file (full path required)

    > python run.py --config-file $PWD/my_config.py

Load application into interactive python session

    > python app.py --cli

Run unit tests

    > python runtests.py