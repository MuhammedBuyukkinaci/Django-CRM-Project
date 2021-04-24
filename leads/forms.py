from django import forms

from .models import Lead

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
        )


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username":UsernameField}

class AssignAgentForm(forms.Form):
    # agent = forms.ChoiceField(choices=(
    #     ('Agent 1 in DB','Agent 1 shown'),
    #     ('Agent 2 in DB','Agent 2 shown'),
    # ))
    agent = forms.ModelChoiceField(queryset= Agent.objects.none())

    def __init__(self,*args,**kwargs):
        request = kwargs.pop("request")
        print(request.user)
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm,self).__init__(*args,**kwargs)
        self.fields["agent"].queryset = agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )
