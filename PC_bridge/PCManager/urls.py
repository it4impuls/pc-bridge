from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addpc/', views.addPC, name='addPC'),
    path('<int:pcId>/', views.detail, name='detail'),
    path('addpc/submit', views.submit, name='submit'),
    path('<int:pcId>/remove', views.remove, name='remove'),
]