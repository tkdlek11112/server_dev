from django.conf.urls import url
from . import views


urlpatterns = [
    url('create', views.TaskCreate.as_view(), name='create'),
    url('delete', views.TaskDelete.as_view(), name='delete'),
    url('select', views.TaskSelect.as_view(), name='select'),
    url('toggle', views.TaskToggle.as_view(), name='toggle'),
    url('', views.Todo.as_view(), name='todo')
]
