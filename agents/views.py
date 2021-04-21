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

class AgentListView(LoginRequiredMixin, ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(LoginRequiredMixin,CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self,form):
        agent = form.save(commit=Fallse)
        agent.organisation = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(LoginRequiredMixin,DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    def get_queryset(self):
        return Agent.objects.all()

    # we don't need form_valid like AgentCreateView

class AgentDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")
        
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)