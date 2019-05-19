from django.http import JsonResponse
from django.urls import resolve
from django.utils.timezone import now

from client_audit.models import Limit, UserActions


def audit_middleware(get_response):

    def store_action(request, blocked):
        namespace = resolve(request.path).route
        UserActions.objects.create(
            route=namespace,
            method=request.method,
            data=request.body,
            ip_address=request.META['REMOTE_ADDR'],
            token='token_madness',
            user=None,
            accepted=not blocked
        )

    def check_limit(request):
        ip = request.META['REMOTE_ADDR']
        namespace = resolve(request.path).route
        for limit in Limit.objects.filter(action=namespace, action_method=request.method):
            kdf = limit.get_operation()(list(map(lambda x: getattr(x, limit.metric_prop), UserActions.objects.filter(
                route=limit.metric,
                method=limit.metric_method,
                ip_address=ip,
                created_at__gte=now()-limit.time_frame,
                accepted=True
            ))))
            print(limit.condition, limit.value, kdf, limit.get_comparison())
            if limit.get_comparison()(limit.value, kdf):
                return True, limit
        return False, Limit.objects.all().first()

    def middleware(request):

        blocked, limit = check_limit(request)

        store_action(request, blocked)

        if blocked:
            return JsonResponse({"message": limit.error_message}, status=limit.error_code)

        response = get_response(request)

        return response

    return middleware
