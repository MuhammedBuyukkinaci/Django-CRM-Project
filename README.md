1) Install Django(Robert Solis) and Django Template by bibhasdn on VSCode.

2) Run the following commands to create an environment, then activate, then install django==3.1.4 and put the packages installed in the nevironment into a yaml file.

```
conda create --name django_crm_env python=3.8
conda activate django_crm_env
pip install django==3.1.4
conda env export | grep -v "^prefix: " > environment.yml
```
3) Create the djcrm project inside the folder we are working.

```
django-admin startproject djcrm .
```

4) Google "Python Gitignore" and put the content of first result in *.gitignore* file.

5) Run the followings to run the project first and migrate default changes

```
python manage.py runserver
python manage.py migrate
```

6) asgi.py enables us to run our server asynchronously.

7) wsgi.py enables us to run our server asynchronously.

8) Create leads app

```
python manage.py startapp leads
```

9) Django is designed to be composed of many apps like 1 app for billing, one app for registration etc.

10) When a model is defined in an app, a table whose name is APPNAME_MODELNAME is created in the DB after makemigrations and migrate. FOr instance, polls_question and polls_choice.

11) In models.py, source is a field which may take elements of SOURCE_CHOICES tuple or any any other entered text.

12) on_delete argument of models.ForeignKey is telling us what to do in case related element(Agent here) is deleted.

13) It is highly recommended to use your own custom User model in models.py

14) Add `AUTH_USER_MODEL = 'leads.User'` to djcrm/settings.py to tell that leads.User is the authenticated user.

15) In leads/models.py, One User map to one agent thanks to models.OneToOneField

16) Model managers work in this way: 

```
Car.objects.all()
Car.objects.filter(make="Audi")# outputing rows whose make column is Audi
Car.objects.filter(year__gt=2016)> year grater than 2016
User.object.get(username="matt")#return only one object
```

17) Create a superuser on Terminal and register Lead, User, Agent in leads/admin.py



