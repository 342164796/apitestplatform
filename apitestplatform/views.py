from django.shortcuts import render
from base.views import plan_index


def index(request):
    return render(request, "base.html")



