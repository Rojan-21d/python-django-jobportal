from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .forms import UpdateCompanyForm
from .models import Company

class UpdateCompanyView(UpdateView):
    form_class = UpdateCompanyForm
    template_name = 'company/update_company.html'
    success_url = reverse_lazy('dashboard')  # Redirect URL after successful update

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to create a job.')
            return redirect('home')  # Redirect to the home page

        # Check if the user is a recruiter
        if not request.user.is_recruiter:
            messages.warning(request, 'Permission denied.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Get the company object related to the logged-in user
        return get_object_or_404(Company, user=self.request.user)

    def form_valid(self, form):
        # Save the form and update the user's company status
        var = form.save(commit=False)
        user = self.request.user
        user.has_company = True  # Set has_company to True
        var.save()  # Save the company
        user.save()  # Save the user
        messages.info(self.request, 'Company info updated successfully!')
        return super().form_valid(form)  # Redirects to the success URL

    def form_invalid(self, form):
        messages.warning(self.request, 'Error in updating company.')
        return super().form_invalid(form)


# view company details
from django.http import Http404

def company_details(request, pk):
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        raise Http404("Company does not exist.")
    context = {'company': company}
    return render(request, 'company/company_details.html', context)
