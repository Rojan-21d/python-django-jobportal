from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Resume
from users.models import User
from .forms import UpdateResumeForm

def update_resume(request):
    if request.user.is_applicant:
        try:
            resume = Resume.objects.get(user=request.user)
        except Resume.DoesNotExist:
            resume = None

        if request.method == "POST":
            form = UpdateResumeForm(request.POST, instance=resume)
            if form.is_valid():
                var = form.save(commit=False)
                var.user = request.user  # Ensure the resume is linked to the current user
                var.email = request.user.email  # Ensure the email is the user's email
                var.save()
                user = User.objects.get(pk=request.user.id)
                user.has_resume = True
                user.save()
                messages.success(request, "Resume Updated Successfully!")
                return redirect("dashboard")
            else:
                messages.error(request, "Error Updating Resume")
        else:
            form = UpdateResumeForm(instance=resume)

        context = {"form": form}
        return render(request, "resume/update_resume.html", context)
    else:
        messages.warning(request, 'Permission Denied!')
        return redirect('dashboard')


def resume_details(request, pk):
    resume = Resume.objects.get(pk=pk)
    return render(request, "resume/resume_details.html", {"resume": resume})
