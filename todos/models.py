from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    """
    Modelo para representar un ToDo/Pendiente
    Compatible con la estructura del API de JSONPlaceholder
    """
    # ID único del todo (puede venir del API externo)
    external_id = models.IntegerField(unique=True, null=True, blank=True, 
                                    help_text="ID del todo en el API externo")
    
    # Usuario propietario del todo
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                           help_text="Usuario propietario del todo")
    
    # Título del todo
    title = models.CharField(max_length=500, help_text="Título del pendiente")
    
    # Estado de completado
    completed = models.BooleanField(default=False, help_text="¿Está completado el todo?")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['external_id', 'id']
        verbose_name = "Todo/Pendiente"
        verbose_name_plural = "Todos/Pendientes"
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.title[:50]}..." if len(self.title) > 50 else f"{status} {self.title}"
    
    @property
    def is_resolved(self):
        """Alias para completed - más semántico en español"""
        return self.completed
    
    @property
    def is_pending(self):
        """Retorna True si el todo está pendiente"""
        return not self.completed
