from django.shortcuts import redirect, render
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
        
        company = None
        if request.user.is_authenticated and request.user.is_recruiter and request.user.has_company:
            company = request.user.company
        
        context = {
            'title': 'Home',
            'jobs': jobs,
            'categories': categories,
            'company': company,
        }
        return render(request, self.template_name, context)

class JobListByCategoryView(ListView):
    model = Job
    template_name = "home/job_list.html"
    context_object_name = "jobs"
    paginate_by = 5

    def get_queryset(self):
        return Job.objects.filter(
            is_available=True,
            category__id=self.kwargs["category_id"]
        ).order_by("-uploaded_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(
            available_jobs_count=Count('job', filter=Q(job__is_available=True))
        ).filter(available_jobs_count__gt=0).order_by('-available_jobs_count')

        context['title'] = 'Jobs by Category'
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
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        try:
            jobs = paginator.page(page_number)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        context['jobs'] = jobs
        categories = Category.objects.annotate(
            available_jobs_count=Count('job', filter=Q(job__is_available=True))
        ).filter(available_jobs_count__gt=0).order_by('-available_jobs_count')
        context['categories'] = categories
        context['title'] = "Job list"
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'home/job_details.html'
    context_object_name = 'job'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.object
        user = self.request.user

        context['title'] = 'Job Details'
        context['a_applicant'] = user.is_authenticated and user.is_applicant
        context['a_recruiter'] = user.is_authenticated and user.is_recruiter

        if context['a_applicant']:
            application = ApplyJob.objects.filter(job=job, user=user).first()
            
            if application:
                context['has_applied'] = True
                context['application_status'] = application.status
            else:
                context['has_applied'] = False
                context['application_status'] = None 
        else:
            context['has_applied'] = False
            context['application_status'] = None

        return context


class JobSearchView(View):
    template_name = "home/job_list.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        category_id = request.GET.get('category', None)

        job_list = Job.objects.filter(is_available=True)

        if query:
            job_list = job_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(work_mode__icontains=query) |
                Q(city__icontains=query) |
                Q(company__name__icontains=query) |  
                Q(category__name__icontains=query) |  
                Q(job_type__icontains=query) |  
                Q(state__name__icontains=query) |  
                Q(edu_level__icontains=query) |  
                Q(experience__name__icontains=query) 
            )

        if category_id:
            job_list = job_list.filter(category__id=category_id)

        job_list = job_list.order_by("-uploaded_date")

        # Pagination logic
        page = request.GET.get("page", 1)
        paginator = Paginator(job_list, 5)
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        categories = Category.objects.annotate(
            available_jobs_count=Count('job', filter=Q(job__is_available=True))
        ).filter(available_jobs_count__gt=0).order_by('-available_jobs_count')

        return render(
            request, 
            self.template_name, 
            {
                "title": "Job Search",
                "page_obj": jobs,  # for pagination part
                "jobs": jobs,
                "query": query,
                "categories": categories, 
                "selected_category": category_id
            }
        )
