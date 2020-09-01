from django.http import HttpResponse
from django.shortcuts import render
def first(request):
    return render(request,'first.html')


