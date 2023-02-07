from django.shortcuts import render  # to render pages
from django.http import HttpResponse  # to send httpResponse to requests
from rango.models import Category # to import the categories set in the model
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect


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
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['page_views'] = page_list
    #render the respsonse and send it back
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')
    # return HttpResponse("Rango says here is the about page.\n <a href='/rango/'>Index</a>")


def show_category(request, category_name_slug):
    #creating a context dictionary which we will pass to the render engine
    context_dict={}

    try:
        category= Category.objects.get(slug=category_name_slug)
        pages= Page.objects.filter(category=category)
        context_dict['pages']= pages
        context_dict['category']=category
    except Category.DoesNotExist:
        context_dict['category']=None
        context_dict['pages']=None

    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    # a HTTP Post
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #have we been provided with a valid form
        if form.is_valid():
            #save the new category in the database
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango')
        else:
            #the supplied form contains error-
            #just print them in the terminal
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})
