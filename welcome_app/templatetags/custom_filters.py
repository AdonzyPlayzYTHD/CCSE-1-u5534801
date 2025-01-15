from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def sum_total(items):
    total = 0
    for item in items:
        total += item.quantity * item.product.price
    return round(total, 2)
