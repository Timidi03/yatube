from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreatinForm

import datetime as dt


class SignUp(CreateView):
    form_class = CreatinForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    

    
    


    
