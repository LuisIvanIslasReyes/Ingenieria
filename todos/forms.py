from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    """Formulario para crear y editar Todos"""
    
    class Meta:
        model = Todo
        fields = ['title', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el título del pendiente...',
                'required': True
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Título del Pendiente',
            'completed': 'Completado'
        }
        help_texts = {
            'title': 'Describe brevemente lo que necesitas hacer',
            'completed': 'Marca si ya completaste esta tarea'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 3:
            raise forms.ValidationError('El título debe tener al menos 3 caracteres.')
        return title.strip()

class TodoSearchForm(forms.Form):
    """Formulario para buscar todos"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar en títulos...'
        })
    )
    
    status = forms.ChoiceField(
        choices=[
            ('all', 'Todos'),
            ('pending', 'Pendientes'),
            ('completed', 'Completados')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class TodoBulkActionForm(forms.Form):
    """Formulario para acciones en lote"""
    action = forms.ChoiceField(
        choices=[
            ('complete', 'Marcar como completados'),
            ('uncomplete', 'Marcar como pendientes'),
            ('delete', 'Eliminar seleccionados')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    selected_todos = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )
