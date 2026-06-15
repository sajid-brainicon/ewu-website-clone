from django.contrib.auth.decorators import login_required, permission_required

from .models import ManagedModule


def require_perm(perm):
    def decorator(view_func):
        return login_required(login_url='/login/')(
            permission_required(perm, raise_exception=True)(view_func)
        )
    return decorator


def has_admin_dashboard_access(user):
    if user.is_superuser or user.is_staff:
        return True
    model_names = ManagedModule.objects.filter(is_active=True).values_list(
        'content_type__model', flat=True
    )
    return any(user.has_perm(f'main.view_{m}') for m in model_names)