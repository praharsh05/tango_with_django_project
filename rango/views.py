from django.shortcuts import render  # to render pages
from django.http import HttpResponse  # to send httpResponse to requests
from rango.models import Category # to import the categories set in the model


def index(request):
    # context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    # return HttpResponse("Rango says Hey there partner!")
    # return HttpResponse("Rango says hey there partner!\n Rango says here is the 
    # index page \n  <a href='/rango/about/'>About</a>")

    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    #render the respsonse and send it back
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')
    # return HttpResponse("Rango says here is the about page.\n <a href='/rango/'>Index</a>")
