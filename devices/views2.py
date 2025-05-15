from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .models import LoginDevice, VisitorFingerprint

@login_required
def my_devices(request):
    devices = LoginDevice.objects.filter(user=request.user).order_by('-login_time')
    return render(request, 'devices/my_devices.html', {'devices': devices})

@login_required
def fingerprint_log_overzicht(request):
    logs = VisitorFingerprint.objects.all().order_by('-timestamp')
    return render(request, 'devices/log_overzicht.html', {'logs': logs})

@login_required
def fingerprint_log_detail(request, key):
    log = get_object_or_404(VisitorFingerprint, id=key)

    return render(request, 'devices/log_detail.html', {'log': log})

@csrf_exempt
def collect_fingerprint(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")

    try:
        data = json.loads(request.body)

        VisitorFingerprint.objects.create(
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            path=request.META.get('PATH_INFO'),
            screen_width=data.get('screen_width'),
            screen_height=data.get('screen_height'),
            language=data.get('language'),
            platform=data.get('platform'),
            timezone=data.get('timezone'),
        )

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'fail', 'error': str(e)})