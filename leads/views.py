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
from django.views.generic import FormView

from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .forms import AssignAgentForm 

from django.contrib.auth.mixins import LoginRequiredMixin

from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Category
from .forms import LeadCategoryUpdateForm

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


class LeadListView(LoginRequiredMixin,ListView):
    template_name = "leads/lead_list.html"
    #queryset is the objects sent to templates.
    #If the name isn't specified, its name is object_list
    context_object_name = "leads"
    
    # Initial queryset of leads for the entire organisation
    def get_queryset(self):
        # self.request.user is the logged-in users
        user = self.request.user
        if user.is_organisor:
            #Thanks to OnetoOneFİeld, we write user.userprofile
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation,agent__isnull=False)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self,**kwargs):
        context = super(LeadListView,self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
                )
            context.update({
                "unassigned_leads": queryset
            })
        return context

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

class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    
    # Initial queryset of leads for the entire organisation
    def get_queryset(self):
        # self.request.user is the logged-in users
        user = self.request.user
        if user.is_organisor:
            #Thanks to OnetoOneFİeld, we write user.userprofile
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_detail(request,pk):
    lead = Lead.objects.get(id = pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

class LeadCreateView(OrganisorAndLoginRequiredMixin,CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self,form):
        # TODO send email
        lead = form.save(commit = False)
        lead.organisation = self.request.user.userprofile
        lead.save()
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

class LeadUpdateView(OrganisorAndLoginRequiredMixin,UpdateView):
    template_name = "leads/lead_update.html"
    #queryset = Lead.objects.all()
    form_class = LeadModelForm
    def get_queryset(self):
        # self.request.user is the logged-in users
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

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

class LeadDeleteView(OrganisorAndLoginRequiredMixin,DeleteView):
    #DeleteView need a template_name
    template_name = "leads/lead_delete.html"
    def get_success_url(self):
        return reverse("leads:lead-list")
    #queryset = Lead.objects.all()
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    

class AssignAgentView(OrganisorAndLoginRequiredMixin,FormView):
    template_name="leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self,form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)



def lead_delete(request,pk):
    lead = Lead.objects.get(id = pk)
    lead.delete()
    return redirect("/leads")


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin,DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)

    #     leads = self.get_object().leads.all()

    #     context.update({
    #         "leads": leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "leads/lead_category_update.html"
    #queryset = Lead.objects.all()
    form_class = LeadCategoryUpdateForm


    def get_queryset(self):
        # self.request.user is the logged-in users
        user = self.request.user
        if user.is_organisor:
            #Thanks to OnetoOneFİeld, we write user.userprofile
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk":self.get_object().id})


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