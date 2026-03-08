from django.urls import path
from . import views
from .views import Signup, Login

urlpatterns = [
    path('todos/', views.ToDoListCreate.as_view(), name='todo_list'),
    path('todos/<int:pk>', views.ToDoRetrieveUpdateDestroy.as_view(), name='todo_RUD'),
    path('todos/<int:pk>/complete', views.ToDoToggleComplete.as_view()),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
]