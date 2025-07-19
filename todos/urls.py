from django.urls import path
from . import views

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),
    
    # Vistas de listado según los requerimientos
    path('todos/ids/', views.TodoIDsListView.as_view(), name='todo_ids_list'),
    path('todos/full/', views.TodoFullListView.as_view(), name='todo_full_list'),
    path('todos/pending/', views.TodoPendingListView.as_view(), name='todo_pending_list'),
    path('todos/completed/', views.TodoCompletedListView.as_view(), name='todo_completed_list'),
    path('todos/users/', views.TodoUserListView.as_view(), name='todo_user_list'),
    path('todos/completed-users/', views.TodoCompletedUserListView.as_view(), name='todo_completed_user_list'),
    path('todos/pending-users/', views.TodoPendingUserListView.as_view(), name='todo_pending_user_list'),
    
    # CRUD Operations
    path('todos/create/', views.todo_create, name='todo_create'),
    path('todos/<int:pk>/update/', views.todo_update, name='todo_update'),
    path('todos/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('todos/<int:pk>/toggle/', views.todo_toggle_status, name='todo_toggle'),
    
    # API Sync
    path('sync/', views.sync_todos_from_api, name='sync_todos'),
]
