from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Job, ApplyJob
from .forms import CreateJobForm, UpdateJobForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# create a job 
class CreateJobView(CreateView):
    form_class = CreateJobForm
    template_name = 'job/create_job.html'
    success_url = reverse_lazy('dashboard')  # Redirect URL after successful job creation

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to create a job.')
            return redirect('home')  # Redirect to the home page

        # Check if the user is a recruiter and has a company
        if not (request.user.is_recruiter and request.user.has_company):
            messages.warning(request, 'Permission Denied!')
            return redirect('dashboard')  # Redirect to the dashboard

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save the form but don't commit to the database yet
        job = form.save(commit=False)

        # Get the category input
        category_name = form.cleaned_data.get('category_name')
        selected_category = form.cleaned_data.get('category')

        # If a category name is provided, check if it already exists or create a new one
        if category_name and not selected_category:
            # Checking if the category already exists
            category, created = Category.objects.get_or_create(name=category_name)
            job.category = category
        else:
            # Use the selected category if one is selected
            job.category = selected_category

        job.user = self.request.user
        job.company = self.request.user.company
        job.save()
        messages.success(self.request, "Job created successfully!")
        return super().form_valid(form)  # Redirects to the success URL

    def form_invalid(self, form):
        messages.warning(self.request, 'There was an error. Please try again.')
        return super().form_invalid(form)


class UpdateJobView(UpdateView):
    form_class = UpdateJobForm
    template_name = 'job/update_job.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to create a job.')
            return redirect('home')
        
        if not (request.user.is_recruiter and request.user.has_company):
            messages.warning(request, 'Permission Denied!')
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Job, pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.save()  
        messages.info(self.request, "Job info updated.")
        return super().form_valid(form)  

    def form_invalid(self, form):
        messages.warning(self.request, 'Something went wrong!')
        return super().form_invalid(form)


class ManageJobsView(ListView):
    model = Job
    template_name = 'job/manage_jobs.html'
    context_object_name = 'jobs'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')

        if not (request.user.is_recruiter and request.user.has_company):
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user, company=self.request.user.company).order_by('-uploaded_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pagination logic (though not typically needed for jobs managed)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['jobs'], 5)  # Use 'jobs' for pagination
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)
        
        context['jobs'] = jobs  # Update the context with paginated jobs
        context["page_obj"] = jobs  # Return page_obj for template pagination
        
        return context

class ApplyToJobView(View):
    def post(self, request, pk):
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}, Is Applicant: {request.user.is_applicant}")

        # Check if the user is authenticated and is an applicant
        if not request.user.is_authenticated or not request.user.is_applicant:
            messages.warning(request, 'You must be logged in as applicant to apply for a job.')
            return redirect('login')

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
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        job = get_object_or_404(Job, pk=self.kwargs['pk'])
        return job.applyjob_set.all()  # Get all applicants for the specific job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])

        # Pagination logic
        page = self.request.GET.get("page", 1)
        paginator = Paginator(context['applicants'], 1)  # Paginate the applicants
        try:
            applicants = paginator.page(page)
        except PageNotAnInteger:
            applicants = paginator.page(1)
        except EmptyPage:
            applicants = paginator.page(paginator.num_pages)
        
        context['applicants'] = applicants  # Update the context with paginated applicants
        return context