from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addpc/', views.addPC, name='addPC'),
    path('<int:pcId>/', views.detail, name='detail'),
    path('addpc/submit', views._submit, name='submit'),
    path('<int:pcId>/remove', views._remove, name='remove'),
    path('<int:pcId>/update', views._update, name='update'),
    path('getstatus', views._getStatus, name='getStatus'),
    path('restart', views._restartPc, name='restart'),
    path('shutdown', views._shutdownPC, name='shutdown'),
    path('pcaction', views._pc_action, name='pcAction'),
]