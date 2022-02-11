from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from .forms import UserCreateForm
# Create your views here.

# This is a little complex because we need to detect when we are
# running in various configurations

class RegisterView(View): #poner esto en una app nueva que se llama authentications
    # Create your views here.

    def register(response):
        if response.method == "POST":
            form = UserCreateForm(response.POST)
            if form.is_valid():
                print("entra")
                form.save()

            return redirect("/")
        else:
            form = UserCreateForm()

        return render(response, "registration/signup.html", {"form": form})
