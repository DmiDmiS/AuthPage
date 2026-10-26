from django.shortcuts import render
import time
import structlog
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = structlog.get_logger(__name__)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'anonymous')
        logger.warning("user_login_failed_mock", username=username, remote_ip=request.META.get('REMOTE_ADDR'))
        return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=401)
    return HttpResponse("Please use POST to login.", status=405)

def health_check(request):
    # Этот эндпоинт будет вызывать Kubernetes для проверки жизнеспособности пода
    return JsonResponse({"status": "healthy", "timestamp": time.time()})

def cpu_stress(request):
    # Наш кастомный SRE-инструмент для вызова авариной нагрузки
    duration = int(request.GET.get('seconds', 10))
    logger.warning("cpu_stress_triggered", duration_seconds=duration)
    
    timeout = time.time() + duration
    while True:
        if time.time() > timeout:
            break
        _ = 5000 * 5000  # Нагружаем CPU вычислениями
        
    return JsonResponse({"status": "stress_test_completed", "duration": duration})

def home_view(request):
    return HttpResponse("Welcome to SRE Auth Portal! Use /api/login or /health", content_type="text/plain")
# Create your views here.
