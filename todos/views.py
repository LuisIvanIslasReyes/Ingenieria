from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm
from .services import TodoAPIService
import requests

# Vista para listar todos los pendientes (solo IDs)
class TodoIDsListView(ListView):
    model = Todo
    template_name = 'todos/todo_ids_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        return Todo.objects.all().order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = Todo.objects.count()
        context['completed_count'] = Todo.objects.filter(completed=True).count()
        context['pending_count'] = Todo.objects.filter(completed=False).count()
        return context

# Vista para listar todos los pendientes (IDs y Titles)
class TodoFullListView(ListView):
    model = Todo
    template_name = 'todos/todo_full_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        return Todo.objects.all().order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = Todo.objects.count()
        context['completed_count'] = Todo.objects.filter(completed=True).count()
        context['pending_count'] = Todo.objects.filter(completed=False).count()
        if context['total_count'] > 0:
            context['completion_percentage'] = round((context['completed_count'] / context['total_count']) * 100, 1)
        else:
            context['completion_percentage'] = 0
        return context

# Vista para pendientes sin resolver (ID y Title)
class TodoPendingListView(ListView):
    model = Todo
    template_name = 'todos/todo_pending_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        return Todo.objects.filter(completed=False).order_by('id')

# Vista para pendientes resueltos (ID y Title)
class TodoCompletedListView(ListView):
    model = Todo
    template_name = 'todos/todo_completed_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        return Todo.objects.filter(completed=True).order_by('id')

# Vista para todos los pendientes (IDs y userID)
class TodoUserListView(ListView):
    model = Todo
    template_name = 'todos/todo_user_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        return Todo.objects.all().order_by('id')

# Vista para pendientes resueltos (ID y userID)
class TodoCompletedUserListView(ListView):
    model = Todo
    template_name = 'todos/todo_completed_user_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        return Todo.objects.filter(completed=True).order_by('id')

# Vista para pendientes sin resolver (ID y userID)
class TodoPendingUserListView(ListView):
    model = Todo
    template_name = 'todos/todo_pending_user_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        return Todo.objects.filter(completed=False).order_by('id')

# CRUD Views
@login_required
def todo_create(request):
    """Crear un nuevo todo"""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, '¡Todo creado exitosamente!')
            return redirect('todo_full_list')
    else:
        form = TodoForm()
    
    return render(request, 'todos/todo_form.html', {
        'form': form, 
        'title': 'Crear Nuevo Todo'
    })

@login_required
def todo_update(request, pk):
    """Actualizar un todo existente"""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Todo actualizado exitosamente!')
            return redirect('todo_full_list')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todos/todo_form.html', {
        'form': form, 
        'title': 'Actualizar Todo',
        'todo': todo
    })

@login_required
def todo_delete(request, pk):
    """Eliminar un todo"""
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo eliminado exitosamente!')
        return redirect('todo_full_list')
    
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})

@login_required
@require_http_methods(["POST"])
def todo_toggle_status(request, pk):
    """Toggle del estado de un todo (completado/pendiente)"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    
    status = "completado" if todo.completed else "pendiente"
    messages.success(request, f'Todo marcado como {status}!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'completed': todo.completed})
    
    return redirect(request.META.get('HTTP_REFERER', 'todo_full_list'))

def sync_todos_from_api(request):
    """Sincronizar todos desde el API externo"""
    service = TodoAPIService()
    
    try:
        synced_count = service.sync_all_todos()
        messages.success(request, f'Se sincronizaron {synced_count} todos desde el API!')
    except Exception as e:
        messages.error(request, f'Error al sincronizar: {str(e)}')
    
    return redirect('todo_full_list')

def dashboard(request):
    """Dashboard principal con resumen de todos"""
    context = {
        'total_todos': Todo.objects.count(),
        'pending_todos': Todo.objects.filter(completed=False).count(),
        'completed_todos': Todo.objects.filter(completed=True).count(),
        'recent_todos': Todo.objects.order_by('-created_at')[:5]
    }
    return render(request, 'todos/dashboard.html', context)
