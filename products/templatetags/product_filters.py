from django import template

register = template.Library()

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

@register.filter
def percentage(value, total):
    """Calculate percentage"""
    try:
        value_float = float(value)
        total_float = float(total)
        if total_float == 0:
            return 0
        return (value_float / total_float) * 100
    except (ValueError, TypeError):
        return 0

@register.filter
def stock_status(product, avg_quantity):
    """Determine stock status based on quantity"""
    try:
        quantity = float(product.quantity)
        avg = float(avg_quantity)
        
        if avg == 0:
            return "unknown"
        
        if quantity < avg * 0.1:
            return "low"
        elif quantity < avg * 0.5:
            return "medium"
        else:
            return "high"
    except (ValueError, TypeError):
        return "unknown"

@register.filter
def stock_status_text(product, avg_quantity):
    """Get stock status text"""
    status = stock_status(product, avg_quantity)
    status_map = {
        "low": "Kam qolgan",
        "medium": "O'rtacha", 
        "high": "Ko'p qolgan",
        "unknown": "Noma'lum"
    }
    return status_map.get(status, "Noma'lum")

@register.filter
def stock_status_color(product, avg_quantity):
    """Get stock status color classes"""
    status = stock_status(product, avg_quantity)
    color_map = {
        "low": "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
        "medium": "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
        "high": "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
        "unknown": "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200"
    }
    return color_map.get(status, "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200")

@register.filter
def stock_status_icon(product, avg_quantity):
    """Get stock status icon"""
    status = stock_status(product, avg_quantity)
    icon_map = {
        "low": "fa-exclamation-triangle",
        "medium": "fa-minus-circle", 
        "high": "fa-check-circle",
        "unknown": "fa-minus"
    }
    return icon_map.get(status, "fa-minus")