from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import Lead

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


def lead_detail(request,pk):
    lead = Lead.objects.get(id = pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)