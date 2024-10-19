from django.shortcuts import redirect, render
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'