from django.contrib import admin
from django.urls import path, include 
from myapp.views import index
from userprofile.views import signup,LogoutView
from django.contrib.auth import views

urlpatterns = [
    path('', index,name="index"),    
    path('invoice/', include("invoice.urls")),
    path('myapp/', include("myapp.urls")),
    path('sign-up/',signup,name="signup"),
    # using django default (builtin) class base views and inherit the template
    path('log-in/',views.LoginView.as_view(template_name="userprofile/login.html"), name="login"),
    path("log-out/",LogoutView.as_view(),name="logout"),
    path('admin/', admin.site.urls),
]
