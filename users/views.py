from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from company.models import Company
from .models import User
from .forms import RegisterUserForm
from resume.models import Resume


# register applicants only
def register_applicant(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_applicant = True
            var.username = var.email
            var.save()
            Resume.objects.create(user=var)
            messages.info(request, "Registration successful. Please login.")
            return redirect("login")
        else:
            messages.error(request, "Invalid form data")
            return redirect("register-applicant")
    else:
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, "users/register_applicant.html", context)


# resigter recruiter only
def register_recruiter(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_recruiter = True
            var.username = var.email
            var.save()
            Company.objects.create(user=var)
            messages.info(request, "Registration successful. Please login.")
            return redirect("login")
        else:
            print(form.errors)  # For debugging form errors
            messages.error(request, "Invalid form data")
            return redirect("register-recruiter")
    else:
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, "users/register_recruiter.html", context)

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            user = authenticate(
                request, username=user.username, password=password
            )  # Authenticate using username

            if user is not None:
                if user.is_active:
                    login(request, user)  # Log the user in
                    return redirect(
                        "dashboard"
                    )  # Redirect to the dashboard or intended page
                else:
                    messages.error(
                        request, "Your account is inactive. Please contact support."
                    )
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(
                request, "Invalid email"
            )  # Handle case when user does not exist

        return redirect("login")  # Redirect to login on error

    else:
        form = AuthenticationForm()  # Create a blank form for GET request
        return render(request, "users/login.html", {"form": form})


# logout User
def logout_user(request):
    logout(request)
    messages.info(request, "Logout Sucessfully")
    return redirect("login")
