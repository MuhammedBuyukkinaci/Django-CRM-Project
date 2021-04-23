from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse

from leads.models import Agent
from .forms import AgentModelForm
from django.core.mail import send_mail

from .mixins import OrganisorAndLoginRequiredMixin

import random

#class AgentListView(LoginRequiredMixin, ListView):
class AgentListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

#class AgentCreateView(LoginRequiredMixin,CreateView):
class AgentCreateView(OrganisorAndLoginRequiredMixin,CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self,form):
        agent = form.save(commit=Fallse)
        user.is_agent = True
        user.is_organisor = False
        #Password must be string
        user.set_password("{}".format(random.randint(0,1000000)))
        user.save()
        Agent.objects.create(
            user=user,
            organisation= self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView,self).form_valid(form)

#class AgentDetailView(LoginRequiredMixin,DetailView):
class AgentDetailView(OrganisorAndLoginRequiredMixin,DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

#class AgentUpdateView(LoginRequiredMixin,UpdateView):
class AgentUpdateView(OrganisorAndLoginRequiredMixin,UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    def get_queryset(self):
        return Agent.objects.all()

    # we don't need form_valid like AgentCreateView

#class AgentDeleteView(LoginRequiredMixin,DeleteView):
class AgentDeleteView(OrganisorAndLoginRequiredMixin,DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")
        
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

