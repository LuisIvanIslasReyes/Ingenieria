import requests
from django.contrib.auth.models import User
from .models import Todo
from django.conf import settings

class TodoAPIService:
    """Servicio para interactuar con el API externo de todos"""
    
    def __init__(self):
        # URL del API de JSONPlaceholder como ejemplo
        self.base_url = "https://jsonplaceholder.typicode.com"
        
    def get_todos_from_api(self):
        """Obtener todos los todos desde el API externo"""
        try:
            response = requests.get(f"{self.base_url}/todos")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener todos del API: {e}")
            return []
    
    def get_todo_by_id(self, todo_id):
        """Obtener un todo específico por ID desde el API"""
        try:
            response = requests.get(f"{self.base_url}/todos/{todo_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener todo {todo_id}: {e}")
            return None
    
    def sync_all_todos(self):
        """Sincronizar todos los todos desde el API"""
        api_todos = self.get_todos_from_api()
        synced_count = 0
        
        for api_todo in api_todos:
            user = self._get_or_create_user(api_todo['userId'])
            
            todo, created = Todo.objects.get_or_create(
                external_id=api_todo['id'],
                defaults={
                    'user': user,
                    'title': api_todo['title'],
                    'completed': api_todo['completed']
                }
            )
            
            if created:
                synced_count += 1
            else:
                # Actualizar si hay cambios
                updated = False
                if todo.title != api_todo['title']:
                    todo.title = api_todo['title']
                    updated = True
                if todo.completed != api_todo['completed']:
                    todo.completed = api_todo['completed']
                    updated = True
                
                if updated:
                    todo.save()
                    synced_count += 1
        
        return synced_count
    
    def _get_or_create_user(self, user_id):
        """Obtener o crear un usuario basado en el ID del API"""
        username = f"api_user_{user_id}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': f'Usuario API {user_id}',
                'email': f'user{user_id}@example.com'
            }
        )
        return user
    
    def sync_user_todos(self, user_id):
        """Sincronizar todos de un usuario específico"""
        try:
            response = requests.get(f"{self.base_url}/users/{user_id}/todos")
            response.raise_for_status()
            api_todos = response.json()
            
            user = self._get_or_create_user(user_id)
            synced_count = 0
            
            for api_todo in api_todos:
                todo, created = Todo.objects.get_or_create(
                    external_id=api_todo['id'],
                    defaults={
                        'user': user,
                        'title': api_todo['title'],
                        'completed': api_todo['completed']
                    }
                )
                
                if created:
                    synced_count += 1
            
            return synced_count
            
        except requests.exceptions.RequestException as e:
            print(f"Error al sincronizar todos del usuario {user_id}: {e}")
            return 0
