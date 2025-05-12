from .models import VisitorFingerprint

class FingerprintMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_superuser:  # Superusers worden niet gelogd
            ip = request.META.get('REMOTE_ADDR')
            ua = request.META.get('HTTP_USER_AGENT', '')
            path = request.path
            VisitorFingerprint.objects.create(ip_address=ip, user_agent=ua, path=path)
        return response
