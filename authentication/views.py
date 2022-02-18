from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from .forms import UserCreateForm
from django.contrib import messages

# Create your views here.

# This is a little complex because we need to detect when we are
# running in various configurations

class RegisterView(View): #poner esto en una app nueva que se llama authentications
    # Create your views here.

    def register(request):

        if request.method == "POST":
            form = UserCreateForm(request.POST)
            if form.is_valid():
                messages.success(request, 'User created successfully.')
                form.save()
            else:
                messages.error(request, 'Invalid form submission.')

                
            #return redirect("/") #mensaje de usuario creado correctamente.
        else:
            form = UserCreateForm()

        return render(request, "registration/signup.html", {"form": form}) #el email se pierde en el redirect