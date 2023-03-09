from django.shortcuts import render,redirect  # to render pages
from django.http import HttpResponse  # to send httpResponse to requests
from rango.models import Category,Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
# from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


# def index(request):
#     # context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
#     # return HttpResponse("Rango says Hey there partner!")
#     # return HttpResponse("Rango says hey there partner!\n Rango says here is the 
#     # index page \n  <a href='/rango/about/'>About</a>")

#     # Query the database for a list of ALL categories currently stored.
#     # Order the categories by the number of likes in descending order.
#     # Retrieve the top 5 only -- or all if less than 5.
#     # Place the list in our context_dict dictionary (with our boldmessage!)
#     # that will be passed to the template engine.
#     category_list = Category.objects.order_by('-likes')[:5]
#     page_list = Page.objects.order_by('-views')[:5]

#     context_dict = {}
#     context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
#     context_dict['categories'] = category_list
#     context_dict['page_views'] = page_list
    
#     #call the helper function to handle the cookies
#     visitor_cookie_handler(request)
#     # context_dict['visits'] = int(request.session['visits'])
#     #obtain our Response object early so we can add cookie information
#     response = render(request,'rango/index.html',context=context_dict)
#     #return the response back to the user, updating any cookies that need changed
#     return response
    
    #render the respsonse and send it back
    # return render(request, 'rango/index.html', context=context_dict)

# def about(request):
#     # if(request.session.test_cookie_worked()):
#     #     print("TEST COOKIE WORKED!")
#     #     request.session.delete_test_cookie()
#     context_dict={}
#     visitor_cookie_handler(request)
#     context_dict['visits'] = int(request.session['visits'])
#     response = render(request,'rango/about.html',context=context_dict)
#     return response
    # return render(request, 'rango/about.html')
    # return HttpResponse("Rango says here is the about page.\n <a href='/rango/'>Index</a>")

# def show_category(request, category_name_slug):
#     #creating a context dictionary which we will pass to the render engine
#     context_dict={}

#     try:
#         category= Category.objects.get(slug=category_name_slug)
#         pages= Page.objects.filter(category=category).order_by('-views')
#         context_dict['pages']= pages
#         context_dict['category']=category
#     except Category.DoesNotExist:
#         context_dict['category']=None
#         context_dict['pages']=None

#     result_list = []
#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         if query:
#             # Run our Bing function to get the results list!
#             context_dict['result_list']=run_query(query)
#             context_dict['query']=query

#     return render(request, 'rango/category.html', context=context_dict)

# @login_required
# def add_category(request):
#     form = CategoryForm()

#     # a HTTP Post
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)

#         #have we been provided with a valid form
#         if form.is_valid():
#             #save the new category in the database
#             form.save(commit=True)
#             # Now that the category is saved, we could confirm this.
#             # For now, just redirect the user back to the index view.
#             return redirect('/rango')
#         else:
#             #the supplied form contains error-
#             #just print them in the terminal
#             print(form.errors)

#     # Will handle the bad form, new form, or no form supplied cases.
#     # Render the form with error messages (if any).
#     return render(request, 'rango/add_category.html', {'form': form})


# @login_required
# def add_page(request, category_name_slug):
#     try:
#         category = Category.objects.get(slug=category_name_slug)
#     except Category.DoesNotExist:
#         category = None

#     if category is None:
#         return redirect('/rango')

#     form =PageForm()

#     if request.method == 'POST':
#         form = PageForm(request.POST)
#         if form.is_valid():
#             if category:
#                 page=form.save(commit=False)
#                 page.category=category
#                 page.view = 0
#                 page.save()

#                 return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
#     else:
#         print(form.errors)
#     context_dict={'form': form, 'category': category}
#     return render(request, 'rango/add_page.html', context= context_dict)


# def register(request):
#     #a boolean value to tell the template if registration was successful
#     registered = False

#     #if HTTP POST we are interested in processing the data
#     if request.method == 'POST':
#         #attempt to grab info from raw form data, making use of both userform and userprofileform
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         #if the two forms are valid
#         if user_form.is_valid() and profile_form.is_valid():
#             #save the user's form data to DB
#             user = user_form.save()
#             #now we hash the password with the set_password method
#             #once hashed we can update the user object
#             user.set_password(user.password)
#             user.save()

#             #now sort out the userprofile instance
#             #since we need to set the user attributes ourselves,
#             # we set commit=False. this delays saving the model
#             # until we are ready to avoid integrity problems

#             profile = profile_form.save(commit=False)
#             profile.user = user

#             #did the user provide a profile picture
#             #if so we need to get it from the input form and,
#             #put it in the UserProfile Model

#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']

#             #now save the UserProfile model instance
#             profile.save()

#             #update the boolean variable to indicate that template,
#             #registration was successful
#             registered=True
        
#         else:
#             #invalid form or forms print problem on terminal
#             print(user_form.errors, profile_form.errors)
#     else:
#         #not a HTTP POST, so we render our form using ModelForm instances,
#         #these forms will be blanck and ready for user input
#         user_form = UserForm()
#         profile_form = UserProfileForm()
    
#     #render the template depending on the context
#     return render(request, 'rango/register.html', context={'user_form':user_form,
#                                                             'profile_form':profile_form,
#                                                             'registered':registered})


# def user_login(request):
#     #if request is an HTTP POST , try to pull out the relavent info
#     if request.method =='POST':
#         # Gather the username and password provided by the user.
#         # This information is obtained from the login form.
#         # We use request.POST.get('<variable>') as opposed
#         # to request.POST['<variable>'], because the
#         # request.POST.get('<variable>') returns None if the
#         # value does not exist, while request.POST['<variable>']
#         # will raise a KeyError exception.
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         #use the Django machinery to check if the username and password
#         #combination is valid, a user object is returned if valid
#         user = authenticate(username = username, password = password)

#         # If we have a User object, the details are correct.
#         # If None (Python's way of representing the absence of a value), no user
#         # with matching credentials was found.
#         if user:
#             #is the account active? it could have been disabled
#             if user.is_active:
#                 #if the account is valid and active we can log the user in
#                 #we will send the user back to homepage
#                 login(request,user)
#                 return redirect(reverse('rango:index'))
#             else:
#                 #an inactive account was used - no longer loging in
#                 return HttpResponse("Your Rango account is disabled.")
#         else:
#             #bad login details were provided, so we can't log user in
#             print(f"Invalid user details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#     #the request is not an HTTP POST so return a login form
#     #this is most likly HTTP GET
#     else:
#         #no context variable to pass to the template system hence blank dict
#         return render(request, 'rango/login.html')


# @login_required
# def restricted(request):
#     # return HttpResponse("since you are logged in, you can see this text!")
#     return render(request,'rango/restricted.html')


#using login_required decorator to ensure only those logged in can access the logout view
# @login_required
# def user_logout(request):
#     #since we know only user that are logged in can use this
#     logout(request)
#     #take the user back to the homepage
#     return redirect(reverse('rango:index'))


# def search(request):
#     result_list = []
#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         if query:
#             # Run our Bing function to get the results list!
#             result_list=run_query(query)

#     return render(request,'rango/search.html', {'result_list': result_list})


# def goto_url(request):
#     page_id=None
#     if request.method == 'GET':
#         page_id = request.GET.get('page_id')
#         try:
#             selected_page = Page.objects.get(id=page_id)
#         except Page.DoesNotExist:
#             return redirect('rango:index')
        
#         selected_page.views = selected_page.views+1
#         selected_page.save()

#         return redirect(selected_page.url)


# @login_required
# def register_profile(request):
#     form = UserProfileForm()


#     if request.method=='POST':
#         form = UserProfileForm(request.POST, request.FILES)

#         if form.is_valid:
#             user_profile=form.save(commit=False)
#             user_profile.user = request.user
#             user_profile.save()

#             return redirect(reverse('rango:index'))
#         else:
#             print(form.errors)
        
#     context_dict={'form':form}
#     return render(request, 'rango/profile_registration.html', context_dict)

class IndexView(View):
    def get(self,request):
        category_list =Category.objects.order_by('-likes')[:5]
        page_list = Page.objects.order_by('-views')[:5]

        context_dict={}
        context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
        context_dict['categories'] = category_list
        context_dict['page_views'] = page_list

        visitor_cookie_handler(request)
        
        return render(request,'rango/index.html', context_dict)

class AboutView(View):
    def get(self,request):
        context_dict ={}
        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']

        return render(request,'rango/about.html', context_dict)

class ShowCategoryView(View):
    def get(self,request,category_name_slug):
        context_dict=self.helper(category_name_slug)
        return render(request, 'rango/category.html', context_dict)
    
    @method_decorator(login_required)
    def post(self,request,category_name_slug):
        context_dict=self.helper(category_name_slug)
        query = request.POST['query'].strip()
        if query:
            context_dict['result_list']=run_query(query)
            context_dict['query']=query
        
        return render(request,'rango/category.html',context_dict)
    
    def helper(self,category_name_slug):
        context_dict = {}
        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')
            context_dict['pages']=pages
            context_dict['category']=category
        except Category.DoesNotExist:
            context_dict['pages']=None
            context_dict['category']=None

        return context_dict

class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
            return render(request, 'rango/add_category.html', {'form': form})

class AddPageView(View):
    def helper(self,category_name_slug):
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category=None
        return category

    @method_decorator(login_required)
    def get(self,request,category_name_slug):
        category=self.helper(category_name_slug)
        if category==None:
            return redirect('/rango')
        else:
            form =PageForm()
            context_dict={'form':form , 'category':category}
            return render(request, 'rango/add_page.html', context_dict)

    @method_decorator(login_required)
    def post(self,request,category_name_slug):
        category = self.helper(category_name_slug)
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category=category
                page.view=0
                page.save()

                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
        return


class RestrictedView(View):
    @method_decorator(login_required)
    def get(self,request):
        return render(request,'rango/restricted.html')


class GotoUrlView(View):
    def get(self,request):
        page_id=request.GET.get('page_id')
        try:
            selected_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect('rango:index')
        
        selected_page.views=selected_page.views+1
        selected_page.save()

        return redirect(selected_page.url)

class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self,request):
        form = UserProfileForm()
        context_dict={'form':form}
        return render(request, 'rango/profile_registration.html', context_dict)

    @method_decorator(login_required)
    def post(self,request):
        form =UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        return

class ProfileView(View):
    def get_user_detail(self,username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website':user_profile.website,
                                'picture':user_profile.picture})
        return (user,user_profile,form)
    
    @method_decorator(login_required)
    def get(self,request,username):
        try:
            (user,user_profile,form) = self.get_user_detail(username)
        except TypeError:
            return redirect('rango:index')
        
        context_dict={'user_profile':user_profile,
                      'selected_user':user,
                      'form':form}
        return render(request,'rango/profile.html',context_dict)
    
    @method_decorator(login_required)
    def post(self,request,username):
        try:
            (user,user_profile,form) = self.get_user_detail(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid:
            form.save(commit=True)
            return redirect('rango:profile', kwargs={'username': username})
        else:
            print(form.errors)

        context_dict={'user_profile':user_profile,
                      'selected_user':user,
                      'form':form}
        return render(request,'rango/profile.html',context_dict)


class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()
        context_dict={'user_profile_list':profiles}
        return render(request,'rango/list_profiles.html', context_dict)


class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self,request):
        category_id = request.GET['category_id']
        try:
            category= Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        category.likes=category.likes+1
        category.save()

        return HttpResponse(category.likes)
    
class CategorySuggestionView(View):
    def get(self,request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion=''
        
        category_list =get_category_list(max_results=8,starts_with=suggestion)
        if len(category_list)==0:
            category_list=Category.objects.order_by('-likes')

        return render(request,'rango/categories.html', {'categories':category_list})

def get_category_list(max_results=0, starts_with=''):
    category_list = []

    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)
    
    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]
    
    return category_list

def visitor_cookie_handler(request):
    #get the number of visits to the site.
    #we use the COOKIES.get() function to obtain the visits cookie
    #is the cookie exists, the value returned is casted to an interger
    #if the cookie doesn;t exist, then the default value of 1 is used
    # visits = int(request.COOKIES.get('visits',1))
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',
                                               str(datetime.now()))

    # last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    #if it has been more than a day since the last visit
    if(datetime.now()-last_visit_time).days >0:
        visits=visits+1
        #update the lst visit cookie now that we have updated the count
        # response.set_cookie('last_visit',str(datetime.now()))
        request.session['last_visit'] = str(datetime.now())
    else:
        #set the last visit cookie
        # response.set_cookie('last_visit',last_visit_cookie)
        request.session['last_visit'] = last_visit_cookie

    #update/set the visits cookie
    # response.set_cookie('visits',visits)
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val=default_val
    return val


