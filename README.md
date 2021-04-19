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
Agent.objects.first()# returns first object
```

17) Create a superuser(admin) on Terminal and register Lead, User, Agent in leads/admin.py

18)  Fill djcrm/urls.py and leads/views.py to return a hellow world when some enters the home page.

19) Update this http response to render function to return a html file.

20) Add templates folder to . directory. Update DIRS key of TEMPLATES variable of djcrm/settings.py .

21) Thanks to context argument of render function in views.py, we are able to send variables from view to template

22) Always define app_name variable in project/urls.py

23) Create lead_detail in leads/views.py and write relevant things in leads/urls.py.

24) In leads/templates/leads/lead_create.html, 

```html
<form method="post" action=".">
        {{form.as_p}}
</form>
```

exist and it means send this form as paragraph to the existent url(. here)

25) csrf_token should be included in forms in html. It is a middleware property for security.

26) In leads/forms.py, It is important to add a comma after the last element of fields attribute of Meta class.

27) To prevent hard coding like href="/leads/create/" in templates, use a pattern with name like `path('create/', lead_create, name = 'lead-create')` in leads/urls.py and use `href="{% url 'leads:lead-create' %}"` in templates while referencing. leads is namespace in djcrm/urls.py and lead-create is name in leads/urls.py

28) Create templates/base.html and templates/scripts.html. These are layout and partial view respectively.

29) Go to Tailwind CSS [this link](https://github.com/aniftyco/awesome-tailwindcss) for awesome css templates.

30) CDN is below. Don't use it in production. In production, use a minified version.

```html
<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">

```

31) Create base.html, landing.html, navbar.html, scripts.html in templates folder. Update the contents in leads/templates/leads to have a better UI using Tailwind CSS.

32) CRUD+L = Create, Retrieve, Update, Delete + List. These are actions that we perform while using models in leads/view.py.

```python
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView

```

33) The 2 codes make the same job. The first one is class-based view and the second one is function-based view.

```python in leads/view.py
class LeadListView(ListView):
    template_name = "leads/lead_list.html"
    #queryset is the objects sent to templates.
    queryset = Lead.objects.all()
    #If the name isn't specified, its name is object_list
    context_object_name = "leads"
```

```python in leads/view.py
def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "leads/lead_list.html",context)
```

34) Convert function based views to Class based view in leads/views.py

35) Create lead_delete.html in leads/templates/leads folder.

36) In production, all of my static files move to static file host provider like digital ocean spaces or amazon s3.

37) Create static folder, create js and css folders in it. Update djcrm/urls.py and djcrm/settings.py and templates/base.html.

38) Build up a system which sends email when a lead is created.

39) To enable login in the project, create templates/registration/login.html . Write relevant code in djcrm/urls.py. Write the line starting with LOGIN_REDIRECT_URL in djcrm/settings.py . Update navbar.html to show which user you are logged in. Make these operations for logout.

40) Django doesn't provide authentication views for signup operation. For signup, create a class named SignupView in leads/views.py . Create signup.html under templates/registration. Then import leads.views.SignupView in djcrm/urls.py. Create a form named CustomUserCreationForm in leads/forms.py and use it in leads/views.py . 









