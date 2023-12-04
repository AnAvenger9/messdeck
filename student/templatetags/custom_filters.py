from django import template
from urllib.parse import quote

register = template.Library()

@register.filter(name='custom_meal_slice')
def custom_meal_slice(value):
    item_tag=value[:10]+" "+value[13:]+" "
    return  item_tag

@register.filter(name='encode')
def encode(value):
    encoded_item_tag = quote(value)
    return encoded_item_tag