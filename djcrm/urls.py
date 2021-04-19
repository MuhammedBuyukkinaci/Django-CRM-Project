"""djcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from leads.views import LandingPageView
# from leads.views import home_page

from django.contrib.auth.views import LoginView 
from django.contrib.auth.views import LogoutView
from leads.views import SignupView
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', LandingPageView.as_view(), name = "landing-page"),
    # Used in function based views:
    # path('', landing_page, name = "landing-page"),
    # namespace is used in templates links like
    # href="{% url 'leads:lead-create' %}"
    path('leads/', include('leads.urls', namespace="leads") ),
    path('signup/', SignupView.as_view(), name="signup" ),
    path('login/', LoginView.as_view(), name="login" ),
    path('logout/', LogoutView.as_view(), name="logout" ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
