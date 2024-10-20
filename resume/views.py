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
    success_url = reverse_lazy('dashboard')

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
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class ResumeDetailView(DetailView):
    model = Resume
    template_name = "resume/resume_details.html"
    context_object_name = 'resume'


# def update_resume(request):
#     if request.user.is_applicant:
#         try:
#             resume = Resume.objects.get(user=request.user)
#         except Resume.DoesNotExist:
#             resume = None

#         if request.method == "POST":
#             form = UpdateResumeForm(request.POST, request.FILES, instance=resume)
#             if form.is_valid():
#                 var = form.save(commit=False)
#                 var.user = request.user  # Ensure the resume is linked to the current user
#                 var.email = request.user.email  # Ensure the email is the user's email
#                 var.save()
#                 user = User.objects.get(pk=request.user.id)
#                 user.has_resume = True
#                 user.save()
#                 messages.success(request, "Resume Updated Successfully!")
#                 return redirect("dashboard")
#             else:
#                 messages.error(request, "Error Updating Resume")
#         else:
#             form = UpdateResumeForm(instance=resume)

#         context = {"form": form}
#         return render(request, "resume/update_resume.html", context)
#     else:
#         messages.warning(request, 'Permission Denied!')
#         return redirect('dashboard')


# def resume_details(request, pk):
#     resume = Resume.objects.get(pk=pk)
#     return render(request, "resume/resume_details.html", {"resume": resume})
