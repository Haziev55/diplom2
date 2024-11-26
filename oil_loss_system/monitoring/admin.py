from django.contrib import admin
from .models import Storage, Loss, Report  # Добавим Report, если хотите работать с отчетами через админку

# Класс для настройки отображения модели Storage
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'temperature', 'pressure')

# Класс для настройки отображения модели Loss
class LossAdmin(admin.ModelAdmin):
    list_display = ('storage', 'loss_type', 'quantity', 'timestamp')

# Класс для настройки отображения модели Report
class ReportAdmin(admin.ModelAdmin):
    list_display = ('storage', 'date', 'total_loss')

# Регистрируем модели с кастомными настройками
admin.site.register(Storage, StorageAdmin)
admin.site.register(Loss, LossAdmin)
admin.site.register(Report, ReportAdmin)
