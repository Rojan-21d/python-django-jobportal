from .models import Resume

def resume_context(request):
    resume = None
    if request.user.is_authenticated and request.user.has_resume:
        resume = Resume.objects.filter(user=request.user).first()
    
    return {'resume': resume}
