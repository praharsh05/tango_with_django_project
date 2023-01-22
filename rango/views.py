from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict={ 'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    # return HttpResponse("Rango says Hey there partner!")
    # return HttpResponse("Rango says hey there partner!\n Rango says here is the index page \n  <a href='/rango/about/'>About</a>")
    return render(request,'rango/index.html', context=context_dict)

def about(request):
    context_dict={ 'boldmessage': 'Praharsh'}
    return render(request, 'rango/about.html', context=context_dict)
    # return HttpResponse("Rango says here is the about page.\n <a href='/rango/'>Index</a>")
