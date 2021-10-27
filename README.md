# django_test_blog
Just a simple example with a bunch of comments.<br>
`Created in educational purposes`<br>

# Structure
There's default django files hierarchy but with a lot comments, which help to find out what specified file do and what relations with other files it have.

# Before start
You need to set up virtual enviroment using your fav python module.

For example, you can set up `virtualenv` with `pip` and create one in convenient place,
or in root of this project.

`pip install virtual env`
`virtualenv venv`, or any other name instead `venv`

Activate your virtual enviroment (using provided scripts in venv-ex-name/Scripts,
`activate.bat` - for windows and CMD, `activate` - for bash / sh or other linux CLI)
And make sure there are appeared a name of venv in parenthesis.

Set up Django
`pip install django`

More likely you will also need to make migrations before server starting
`python ./manage.py makemigrations`

Start server!
`python ./manage.py startserver`

Also you need to know that there is no database in this repo!
You need to add some data by yourself, using Django's REPL mode (manage.py shell) or
website interface (recomended, cause it is only one useful functions of whole project Biblethump)