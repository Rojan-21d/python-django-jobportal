# company/context_processors.py
from .models import Company

def company_context(request):
    company = None
    if request.user.is_authenticated and request.user.has_company:
        company = Company.objects.filter(user=request.user).first()  # or however you link Company to the user
    
    return {'company': company}
