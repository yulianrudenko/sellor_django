from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template import loader


def custom_handler404(request, exception):
    template = loader.get_template('not_found.html')
    body = template.render(request=request)
    return HttpResponseNotFound(body)