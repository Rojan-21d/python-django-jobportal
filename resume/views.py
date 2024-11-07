from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Resume
from users.models import User
from .forms import UpdateResumeForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView


class UpdateResumeView(UpdateView):
    model = Resume
    form_class = UpdateResumeForm
    template_name = "resume/update_resume.html"
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        try:
            return Resume.objects.get(user=self.request.user)
        except Resume.DoesNotExist:
            return None

    def form_valid(self, form):
        # Customize the form validation
        resume = form.save(commit=False)
        resume.user = self.request.user
        resume.email = self.request.user.email
        resume.save()

        user = User.objects.get(pk=self.request.user.id)
        user.has_resume = True
        user.save()

        messages.success(self.request, "Resume Updated Successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error Updating Resume")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_applicant:
            messages.warning(request, 'Permission Denied!')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Resume"
        return context


class ResumeDetailView(DetailView):
    model = Resume
    template_name = "resume/resume_details.html"
    context_object_name = 'resume'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Resume Details"
        return context