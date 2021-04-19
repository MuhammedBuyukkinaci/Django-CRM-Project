from django.shortcuts import render,redirect
from django.shortcuts import reverse
from django.core.mail import send_mail
# Create your views here.

from django.http import HttpResponse

from .models import Lead
from .models import Agent

from .forms import LeadForm, LeadModelForm

from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView

from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

class SignupView(CreateView):
    template_name = "registration/signup.html"
    #form_class = UserCreationForm
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")
    


class LandingPageView(TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request,"landing.html")


class LeadListView(ListView):
    template_name = "leads/lead_list.html"
    #queryset is the objects sent to templates.
    queryset = Lead.objects.all()
    #If the name isn't specified, its name is object_list
    context_object_name = "leads"

def lead_list(request):
    #return HttpResponse("Hello world")
    #return render(request, "leads/home_page.html")
    # context = {
    #     "name": "Yavuz",
    #     "age": 35
    # }

    leads = Lead.objects.all()

    context = {
        "leads": leads
    }
    return render(request, "leads/lead_list.html",context)

class LeadDetailView(DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


def lead_detail(request,pk):
    lead = Lead.objects.get(id = pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

class LeadCreateView(CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self,form):
        # TODO send email
        send_mail(
            subject="a lead has been created",
            message= "Go to the site to view the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView,self).form_valid(form)


def lead_create(request):

    form = LeadModelForm()

    if request.method == "POST":
        # Overwriting form variable if request is POST
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect("/leads")

    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)

class LeadUpdateView(UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request,pk):
    lead = Lead.objects.get(id = pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST,instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }

    return render(request, "leads/lead_update.html", context)

class LeadDeleteView(DeleteView):
    #DeleteView need a template_name
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_delete(request,pk):
    lead = Lead.objects.get(id = pk)
    lead.delete()
    return redirect("/leads")


# Redundant functions
# def lead_update(request,pk):
#     lead = Lead.objects.get(id = pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("/leads")

#     context = {
#         "form": form,
#         "lead": lead
#     }
#     return render(request, "leads/lead_update.html", context)

# def lead_create(request):
#     form = LeadForm()
#     if request.method == "POST":
#         print("Receiving a post request")
#         # Overwriting form variable if request is POST
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print("The form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name = first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             print("The lead has been created")
#             return redirect("/leads")

#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)