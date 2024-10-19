from django.shortcuts import render
from django.views.generic import ListView, DetailView
import job
from job.models import Job, Category, ApplyJob
from django.views import View
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

from django.views.generic import ListView
from django.db.models import Count, Q

class JobListByCategoryView(ListView):
    model = Job
    template_name = "home/job_list.html"
    context_object_name = "jobs"
    paginate_by = 5

    def get_queryset(self):
        return Job.objects.filter(
            is_available=True,
            category__id=self.kwargs["category_id"]  # Get category ID from URL
        ).order_by("-uploaded_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(
            available_jobs_count=Count('job', filter=Q(job__is_available=True))
        ).filter(available_jobs_count__gt=0).order_by('-available_jobs_count')[:20]

        context['categories'] = categories 
        context['selected_category_id'] = self.kwargs["category_id"]
        return context

class JobListingView(ListView):
    model = Job
    template_name = 'home/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 5

    def get_queryset(self):
        return Job.objects.filter(is_available=True).order_by('-uploaded_date')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add pagination to the context
        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), self.paginate_by)

        try:
            jobs = paginator.page(page_number)
        except PageNotAnInteger:
            jobs = paginator.page(1)  # If page is not an integer, deliver first page
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page

        context['jobs'] = jobs  # Update context with paginated jobs
        # Fetch categories for the sidebar
        categories = Category.objects.annotate(
            available_jobs_count=Count('job', filter=Q(job__is_available=True))
        ).filter(available_jobs_count__gt=0).order_by('-available_jobs_count')[:20]
        context['categories'] = categories  # Add categories to the context
        return context



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
    

class JobSearchView(View):
    template_name = "home/job_list.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")
        job_list = Job.objects.filter(
            (
                Q(title__icontains=query) | Q(content__icontains=query)
            ) & Q(is_available=True)
        ).order_by("-uploaded_date")

        # Pagination
        page = request.GET.get("page", 1)
        paginate_by = 5
        paginator = Paginator(job_list, paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(
            request,
            self.template_name,
            {"page_obj": posts, "query": query},
        )
