# FlaskForum

To get the project running on windows

> set FLASK_APP=run.py

> set FLASK_CONFIG=development

To get the project running on *nix

> export FLASK_APP=run.py

> export FLASK_CONFIG=development

After running the commands above create a database called fforum_db and then run the following commands
> flask db migrate

> flask db upgrade

The second command can also be ran to apply any changes to the database. To help with this there is a file called 'db_update' the script has been created for both *nix and Windows environments.

Use of a virtualenv is suggested and all the project requirements have been frozen to requirements. To install the dependancies run
> pip install -r requirements.txt