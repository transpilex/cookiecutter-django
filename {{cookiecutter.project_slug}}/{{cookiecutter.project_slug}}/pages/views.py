from django.shortcuts import render
from django.template import TemplateDoesNotExist
{%- if cookiecutter.use_auth == 'y' %}
from django.contrib.auth.decorators import login_required
{%- endif %}


{%- if cookiecutter.use_auth == 'y' %}
@login_required
{%- endif %}
def root_page_view(request):
    try:
        return render(request, 'pages/index.html')
    except TemplateDoesNotExist:
        return render(request, '404.html')



{%- if cookiecutter.use_auth == 'y' %}
@login_required
{%- endif %}
def dynamic_pages_view(request, template_name):
    try:
        return render(request, f'pages/{template_name}.html')
    except TemplateDoesNotExist:
        return render(request, f'404.html')
