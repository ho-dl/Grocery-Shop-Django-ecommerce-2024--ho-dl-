from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url='login'  # Replace 'login' with your actual login URL name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
