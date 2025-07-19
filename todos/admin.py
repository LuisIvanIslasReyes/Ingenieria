from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'external_id', 'title', 'user', 'completed', 'created_at']
    list_filter = ['completed', 'created_at', 'user']
    search_fields = ['title', 'user__username', 'external_id']
    list_editable = ['completed']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('title', 'user', 'completed')
        }),
        ('API Externa', {
            'fields': ('external_id',),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    actions = ['mark_completed', 'mark_pending']
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f'{updated} todos marcados como completados.')
    mark_completed.short_description = "Marcar seleccionados como completados"
    
    def mark_pending(self, request, queryset):
        updated = queryset.update(completed=False)
        self.message_user(request, f'{updated} todos marcados como pendientes.')
    mark_pending.short_description = "Marcar seleccionados como pendientes"
