from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """
    Decorator that checks if a user is authenticated and is a staff member.
    Redirects to the home page with an error message if the checks fail.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    return wrapper_func