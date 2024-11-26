# oil_loss_system/urls.py
from django.contrib import admin
from django.urls import path
from monitoring import views  # Импорт ваших представлений

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Добавляем путь для главной страницы
    path('monitoring/storages/', views.storage_list, name='storage_list'),
    path('monitoring/loss_prediction/', views.predict_losses, name='loss_prediction'),
    path('monitoring/loss_graph/', views.loss_graph, name='loss_graph'),
]
