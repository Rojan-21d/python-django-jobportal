from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from .models import User
from .forms import RegisterUserForm
from resume.models import Resume
from company.models import Company

class RegisterApplicantView(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register_applicant.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        var = form.save(commit=False)
        var.is_applicant = True
        var.username = var.email
        var.save()
        Resume.objects.create(user=var)
        messages.info(self.request, "Registration successful. Please login.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form data")
        return redirect("register-applicant")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Register Applicant"
        return context


class RegisterRecruiterView(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register_recruiter.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        var = form.save(commit=False)
        var.is_recruiter = True
        var.username = var.email
        var.save()
        Company.objects.create(user=var)
        messages.info(self.request, "Registration successful. Please login.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form data")
        return redirect("register-recruiter")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Register Recruiter"
        return context

class LoginUserView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {"form": form, "title": "Login"}
        return render(request, "users/login.html", context)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user) # session banauxa
                    return redirect("home")
                else:
                    messages.error(request, "Your account is inactive. Please contact support.")
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email")

        return redirect("login")
    
def logout_user(request):
    logout(request)
    messages.info(request, "Logout Successfully")
    return redirect("login")