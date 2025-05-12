
from django.contrib.auth.decorators import login_required
from forum.models import LoginDevice
from django.shortcuts import render


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = x_forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def my_devices(request):
    devices = LoginDevice.objects.filter(user=request.user).order_by('-login_time')
    context = {
        'devices': devices,
        'has_devices': devices.exists()
    }
    return render(request, 'devices/templates/devices.html', context)


