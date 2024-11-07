from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Job, ApplyJob
from .forms import CreateJobForm, UpdateJobForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# create a job 
class CreateJobView(CreateView):
    form_class = CreateJobForm
    template_name = 'job/create_job.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to create a job.')
            return redirect('home')

        if not (request.user.is_recruiter and request.user.has_company):
            messages.warning(request, 'Permission Denied!')
            return redirect('home') 

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save the form but don't commit to the database yet
        job = form.save(commit=False)

        category_name = form.cleaned_data.get('category_name')
        selected_category = form.cleaned_data.get('category')

        if category_name and not selected_category:
            category, created = Category.objects.get_or_create(name=category_name)
            job.category = category
        else:
            job.category = selected_category

        job.user = self.request.user
        job.company = self.request.user.company
        job.save()
        messages.success(self.request, "Job created successfully!")
        return super().form_valid(form)  # Redirects to the success URL

    def form_invalid(self, form):
        messages.warning(self.request, 'There was an error. Please try again.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Post A Job"
        return context

class UpdateJobView(UpdateView):
    form_class = UpdateJobForm
    template_name = 'job/update_job.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to create a job.')
            return redirect('home')
        
        if not (request.user.is_recruiter and request.user.has_company):
            messages.warning(request, 'Permission Denied!')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        return job
    
    def get_success_url(self):
        return reverse_lazy('job-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        try:
            form.save()
            messages.info(self.request, "Job info updated.")
        except Exception as e:
            messages.warning(self.request, f"Something went wrong: {e}")
            print(f"Error: {e}")
            return super().form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Something went wrong!')
        print("Errors:", form.errors) 
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Job"
        return context

class ManageJobsView(ListView):
    model = Job
    template_name = 'job/manage_jobs.html'
    context_object_name = 'jobs'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')

        if not (request.user.is_recruiter and request.user.has_company):
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user, company=self.request.user.company).order_by('-uploaded_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['jobs'], 5)
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)
        
        context['title']  = 'Manage Jobs'
        context['jobs'] = jobs  # Update the context with paginated jobs
        context["page_obj"] = jobs  # Return page_obj for template pagination
        
        return context

class ApplyToJobView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_applicant:
            messages.warning(request, 'You must be logged in as applicant to apply for a job.')
            return redirect('login')
        
        if not request.user.has_resume:
            messages.warning(request, 'You must create a resume first.')
            return redirect('home') 
        
        job = get_object_or_404(Job, pk=pk)
        ApplyJob.objects.create(
            job=job,
            user=request.user,
            status='pending',
        )
        messages.success(request, 'Job applied successfully!')
        return redirect('job-list')

    def get(self, request, pk):
        messages.info(request, "Please submit your application through post method.")
        return redirect('job-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Apply Job"
        return context

class AllApplicantsView(ListView):
    model = ApplyJob
    template_name = 'job/all_applicants.html'
    context_object_name = 'applicants'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to view applicants.')
            return redirect('login')

        if not request.user.is_recruiter:
            messages.warning(request, 'Permission Denied! You are not authorized to view applicants.')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        return job.applyjob_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])

        page = self.request.GET.get("page", 1)
        paginator = Paginator(context['applicants'], 5)
        try:
            applicants = paginator.page(page)
        except PageNotAnInteger:
            applicants = paginator.page(1)
        except EmptyPage:
            applicants = paginator.page(paginator.num_pages)

        context['applicants'] = applicants
        context["title"] = "All Applicants"
        return context

class UpdateApplicationStatusView(View):
    def post(self, request, pk, applicant_pk):
        # Get the application and applicant
        applicant = get_object_or_404(ApplyJob, pk=applicant_pk)

        new_status = request.POST.get('status')

        if new_status in ['approved', 'rejected']:
            applicant.status = new_status
            applicant.save()

            if new_status == 'approved':
                messages.success(request, f'Application for {applicant.user.resume.first_name} {applicant.user.resume.last_name} has been approved.')
            else:
                messages.success(request, f'Application for {applicant.user.resume.first_name} {applicant.user.resume.last_name} has been rejected.')

        return redirect('applicants', pk=pk)


class AppliedJob(ListView):
    model = ApplyJob
    template_name = 'job/applied_job.html'
    context_object_name = 'applied_jobs'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to view your applied jobs.')
            return redirect('login')
        
        if not request.user.is_applicant:
            messages.warning(request, 'Permission Denied! You are not authorized to view your applied jobs.')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ApplyJob.objects.filter(user=self.request.user).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pagination logic
        page = self.request.GET.get("page", 1)
        paginator = Paginator(context['applied_jobs'], 5)  # 5 jobs per page
        try:
            applied_jobs = paginator.page(page)
        except PageNotAnInteger:
            applied_jobs = paginator.page(1)
        except EmptyPage:
            applied_jobs = paginator.page(paginator.num_pages)
        
        context["title"] = "Applied Jobs"
        context['applied_jobs'] = applied_jobs
        context['page_obj'] = applied_jobs 
        
        return context

    def __str__(self):
        return super().__str__() + ' Applied Jobs'

class UpdateJobView(UpdateView):
    form_class = UpdateJobForm
    template_name = 'job/update_job.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to update a job.')
            return redirect('home')

        # Check if the user is a recruiter and has a company
        if not (request.user.is_recruiter and request.user.has_company):
            messages.warning(request, 'Permission Denied!')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Retrieve the job object to be updated
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        return job

    def get_success_url(self):
        # Sending pk
        return reverse_lazy('job-details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Job updated successfully!")
        return super().form_valid(form)  # Redirects to the success URL

    def form_invalid(self, form):
        messages.warning(self.request, 'Something went wrong! Please fix the errors below.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        context['job'] = job
        return context

class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy('manage-job')

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Job"
        return context

