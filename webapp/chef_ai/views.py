from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from .forms import ingredientList

# Create your views here.

def index(request):
    if request.method == "POST":
        form = ingredientList(request.POST)
        if form.is_valid():
            selected_options = form.cleaned_data['choices']
            print("Selected Options: ", selected_options)
            return render(request, 'resp.html', {'selected_options': selected_options})
    else:
        form = ingredientList()
    return render(request, 'test.html', {'form': form})

