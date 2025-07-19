from django import template

register = template.Library()

@register.filter
def count_completed(todos):
    """Cuenta los todos completados en una lista"""
    return sum(1 for todo in todos if todo.completed)

@register.filter
def count_pending(todos):
    """Cuenta los todos pendientes en una lista"""
    return sum(1 for todo in todos if not todo.completed)

@register.filter
def percentage_completed(todos):
    """Calcula el porcentaje de todos completados"""
    total = len(todos)
    if total == 0:
        return 0
    completed = sum(1 for todo in todos if todo.completed)
    return round((completed / total) * 100, 1)
