from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.inclusion_tag('main/menu/menu.html')
def navbar():
    print('test')
    return {'navbar': [
        {
            'label': 'Home',
            'icon': 'home',
            'hx': {
                'get': True,
                'url': reverse_lazy('main:index'),
            }
        }
    ]}
