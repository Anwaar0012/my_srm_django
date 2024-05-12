from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View

from .models import Userprofile
# Create your views here.
def signup(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save() # then save to the database
            # userprofile=Userprofile.objects.create(user=user)
            # not using variable
            Userprofile.objects.create(user=user)
            return redirect('login')
    else:
        # create empty instance 
        form=UserCreationForm()

    return render(request,'userprofile/signup.html',{'form':form})

from django.contrib.auth import logout

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')