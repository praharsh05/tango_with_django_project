from django.shortcuts import render  # to render pages
from django.http import HttpResponse  # to send httpResponse to requests
from rango.models import Category # to import the categories set in the model
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required


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

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango')

    form =PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page=form.save(commit=False)
                page.category=category
                page.view = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
    else:
        print(form.errors)
    context_dict={'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context= context_dict)


def register(request):
    #a boolean value to tell the template if registration was successful
    registered = False

    #if HTTP POST we are interested in processing the data
    if request.method == 'POST':
        #attempt to grab info from raw form data, making use of both userform and userprofileform
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        #if the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            #save the user's form data to DB
            user = user_form.save()
            #now we hash the password with the set_password method
            #once hashed we can update the user object
            user.set_password(user.password)
            user.save()

            #now sort out the userprofile instance
            #since we need to set the user attributes ourselves,
            # we set commit=False. this delays saving the model
            # until we are ready to avoid integrity problems

            profile = profile_form.save(commit=False)
            profile.user = user

            #did the user provide a profile picture
            #if so we need to get it from the input form and,
            #put it in the UserProfile Model

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #now save the UserProfile model instance
            profile.save()

            #update the boolean variable to indicate that template,
            #registration was successful
            registered=True
        
        else:
            #invalid form or forms print problem on terminal
            print(user_form.errors, profile_form.errors)
    else:
        #not a HTTP POST, so we render our form using ModelForm instances,
        #these forms will be blanck and ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    #render the template depending on the context
    return render(request, 'rango/register.html', context={'user_form':user_form,
                                                            'profile_form':profile_form,
                                                            'registered':registered})


def user_login(request):
    #if request is an HTTP POST , try to pull out the relavent info
    if request.method =='POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        #use the Django machinery to check if the username and password
        #combination is valid, a user object is returned if valid
        user = authenticate(username = username, password = password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            #is the account active? it could have been disabled
            if user.is_active:
                #if the account is valid and active we can log the user in
                #we will send the user back to homepage
                login(request,user)
                return redirect(reverse('rango:index'))
            else:
                #an inactive account was used - no longer loging in
                return HttpResponse("Your Rango account is disabled.")
        else:
            #bad login details were provided, so we can't log user in
            print(f"Invalid user details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    #the request is not an HTTP POST so return a login form
    #this is most likly HTTP GET
    else:
        #no context variable to pass to the template system hence blank dict
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return HttpResponse("since you are logged in, you can see this text!")
