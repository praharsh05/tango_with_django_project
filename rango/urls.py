from django.urls import path
from rango import views
from rango.views import AboutView, AddCategoryView, IndexView, ShowCategoryView, AddPageView
from rango.views import RestrictedView, GotoUrlView, RegisterProfileView

app_name='rango'
urlpatterns= [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('category/<slug:category_name_slug>/',
        ShowCategoryView.as_view(), name='show_category'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', AddPageView.as_view(), name='add_page'),
    path('restricted/', RestrictedView.as_view(), name='restricted'),
    path('goto/', GotoUrlView.as_view(), name='goto'),
    path('register_profile/', RegisterProfileView.as_view(), name='register_profile'),
    # path('register/',views.register,name='register'),
    # path('login/', views.user_login,name='login'),
    # path('logout/', views.user_logout, name='logout'),
    # path('search/', views.search, name='search'),
]