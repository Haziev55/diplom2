from django.db import models
import math

# Модель для продуктов нефти
class OilProduct(models.Model):
    name = models.CharField(max_length=100)  # Название продукта
    description = models.TextField()  # Описание продукта

    def __str__(self):
        return self.name


# Модель для хранилищ
class Storage(models.Model):
    name = models.CharField(max_length=100)  # Название хранилища
    capacity = models.FloatField(help_text="Емкость хранилища (в литрах)")  # Емкость
    temperature = models.FloatField(help_text="Температура в хранилище")  # Температура
    pressure = models.FloatField(help_text="Давление в хранилище")  # Давление
    oil_product = models.ForeignKey(OilProduct, on_delete=models.CASCADE)  # Связь с продуктом

    def __str__(self):
        return f"{self.name} ({self.oil_product.name})"


# Модель для потерь
class Loss(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)  # Связь с хранилищем
    loss_type = models.CharField(
        max_length=50, choices=[('Evaporation', 'Испарение'), ('Leak', 'Утечка'),
                               ('Chemical', 'Химический процесс'), ('Physical', 'Физический процесс')]
    )  # Тип потерь
    quantity = models.FloatField(help_text="Количество потерянного продукта (в литрах)")  # Количество
    timestamp = models.DateTimeField(auto_now_add=True)  # Время потерь

    @property
    def calculated_loss(self):
        # Реализация расчетов потерь
        if self.loss_type == 'Evaporation':
            return self.calculate_evaporation_loss()
        elif self.loss_type == 'Leak':
            return self.calculate_leak_loss()
        # Добавьте другие методы для химических и физических процессов
        return self.quantity

    def calculate_evaporation_loss(self):
        evaporation_rate = 0.1
        temperature = self.storage.temperature
        pressure = self.storage.pressure
        surface_area = self.storage.capacity

        # Формула для испарения
        evaporation_loss = evaporation_rate * surface_area * math.exp(-temperature / 100) * (pressure / 1013)
        return evaporation_loss

    def __str__(self):
        return f"{self.loss_type} - {self.quantity}L"


# Модель для отчетов
class Report(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)  # Связь с хранилищем
    date = models.DateField()  # Дата отчета
    total_loss = models.FloatField(help_text="Общие потери за день (в литрах)")  # Общие потери

    def __str__(self):
        return f"Отчет за {self.date} ({self.total_loss}L)"
