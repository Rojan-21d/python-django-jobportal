from .models import Company

def company_context(request):
    company = None
    if request.user.is_authenticated and request.user.has_company:
        company = Company.objects.filter(user=request.user).first()
    
    return {'company': company}
