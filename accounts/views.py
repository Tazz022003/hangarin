from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render


class UserLoginView(LoginView):
    template_name = "accounts/login.html"


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "accounts/signup_success.html")

    else:
        form = UserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})