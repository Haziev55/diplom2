from django.urls import path
from . import views

urlpatterns = [
    path('storages/', views.storage_list, name='storage_list'),
    path('reports/', views.report_list, name='report_list'),
    path('loss_graph/', views.loss_graph, name='loss_graph'),
]
