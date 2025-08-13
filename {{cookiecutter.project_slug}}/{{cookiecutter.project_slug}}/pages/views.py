from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.contrib.auth.decorators import login_required



{%- if cookiecutter.auth == 'y' %}
@login_required
{%- endif %}
def root_page_view(request):
    try:
        return render(request, 'pages/index.html')
    except TemplateDoesNotExist:
        return render(request, 'pages/error-404.html')



{%- if cookiecutter.auth == 'y' %}
@login_required
{%- endif %}
def dynamic_pages_view(request, template_name):
    try:
        return render(request, f'pages/{template_name}.html')
    except TemplateDoesNotExist:
        return render(request, f'pages/error-404.html')
