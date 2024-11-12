from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UpdateCompanyForm
from .models import Company
from django.http import Http404

class UpdateCompanyView(UpdateView):
    form_class = UpdateCompanyForm
    template_name = 'company/update_company.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_recruiter:
            messages.warning(request, 'You must be logged in as a recruiter to update a company.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Company, pk=pk, user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('company-details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        company = form.save(commit=False)
        company.save()
        self.request.user.has_company = True
        self.request.user.save()
        messages.info(self.request, 'Company info updated successfully!')
        return super().form_valid(form) 

    def form_invalid(self, form):
        messages.warning(self.request, 'Error in updating company.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Company"
        return context

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company/company_details.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['a_recruiter'] = user.is_authenticated and user.is_recruiter
        context["title"] = "Company Details"
        return context

    def get_object(self, queryset=None):
        try:
            return Company.objects.get(pk=self.kwargs['pk'])
        except Company.DoesNotExist:
            raise Http404("Company does not exist.")

