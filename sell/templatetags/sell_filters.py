from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide the value by the argument"""
    try:
        arg_float = float(arg)
        if arg_float == 0:
            return 0
        return float(value) / arg_float
    except (ValueError, TypeError):
        return 0

@register.filter
def format_currency(value):
    """Format number as currency with spaces every 3 digits"""
    try:
        value = float(value)
        # Format with spaces every 3 digits
        formatted = "{:,.0f}".format(value).replace(",", " ")
        return f"{formatted}"
    except (ValueError, TypeError):
        return "0"

@register.filter
def format_quantity(value):
    """Format quantity with K, M suffixes"""
    try:
        value = float(value)
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        else:
            return f"{value:.0f}"
    except (ValueError, TypeError):
        return "0"