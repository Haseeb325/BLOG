from django import template

register = template.Library()

# ye is liay kia hamay replies ki dictionary mil rhi thi to idhr decorator banaya jis ka kam hota hai agr koi kam hai to us k sath jp b krna kr lo change krna ya jo
@register.filter(name='get_val')

def get_val(dict ,key):
    return dict.get(key)