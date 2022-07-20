from django.shortcuts import redirect


def redirect_home_if_authenticated(function, *args, **kwargs):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:home')
        return function(request)
    return wrapper


def previous_url_or_other(request, other_url):
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url)
    return redirect(other_url)