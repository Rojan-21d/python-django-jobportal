from django.shortcuts import render
from django.views.generic import ListView, DetailView
from job.models import Job, Category, ApplyJob
from django.views import View
from django.db.models import Count, Q

class HomeView(View):
    template_name = 'home/home.html'
    
    def get(self, request):
        jobs = Job.objects.filter(is_available=True).order_by('-uploaded_date')[:5]

        # Fetch categories ordered by job count and limit to 8
        categories = Category.objects.annotate(
            available_jobs_count=Count('job', filter=Q(job__is_available=True))
        ).filter(available_jobs_count__gt=0).order_by('-available_jobs_count')[:8]
        
        context = {
            'jobs': jobs,
            'categories': categories,
        }
        return render(request, self.template_name, context)

class JobListingView(ListView):
    model = Job
    template_name = 'home/job_list.html'
    context_object_name = 'jobs'
    
    def get_queryset(self):
        return Job.objects.filter(is_available=True).order_by('-uploaded_date')

class JobDetailView(DetailView):
    model = Job
    template_name = 'home/job_details.html'
    context_object_name = 'job'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_available=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.object
        
        # Check if the user has already applied for this job
        if self.request.user.is_authenticated:
            has_applied = ApplyJob.objects.filter(job=job, user=self.request.user).exists()
            context['has_applied'] = has_applied

        return context
