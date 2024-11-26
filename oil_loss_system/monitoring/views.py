from django.shortcuts import render
from .models import Storage, Loss, Report
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64


# Представление для главной страницы
def home(request):
    return render(request, 'monitoring/home.html')


# Представление для списка хранилищ
def storage_list(request):
    storages = Storage.objects.all()
    return render(request, 'monitoring/storage_list.html', {'storages': storages})


# Представление для списка отчетов
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'monitoring/report_list.html', {'reports': reports})


# Представление для предсказания потерь
def predict_losses(request):
    # Собираем данные о потерях (например, по времени, температуре, давлению)
    loss_data = Loss.objects.all().values('timestamp', 'quantity', 'storage__temperature', 'storage__pressure')
    df = pd.DataFrame(loss_data)

    # Преобразуем данные для модели
    X = df[['storage__temperature', 'storage__pressure']]  # Признаки
    y = df['quantity']  # Целевая переменная

    # Обучаем модель
    model = LinearRegression()
    model.fit(X, y)

    # Прогнозируем потери
    df['predicted_loss'] = model.predict(X)

    # Передаем данные в шаблон для отображения
    return render(request, 'monitoring/loss_prediction.html', {'data': df.to_dict('records')})


# Представление для графика потерь
def loss_graph(request):
    losses = Loss.objects.all()
    # Тimestamps - время, когда происходят потери, и quantities - количество потерь
    timestamps = [loss.timestamp for loss in losses]
    quantities = [loss.quantity for loss in losses]

    # Строим график
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, quantities, label='Потери', color='blue')
    plt.xlabel('Время')
    plt.ylabel('Количество потерь (литры)')
    plt.title('График потерь нефти')
    plt.legend()

    # Сохраняем график в буфер
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Преобразуем в base64 для отображения в HTML
    image_data = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Передаем изображение в контекст для шаблона
    return render(request, 'monitoring/loss_graph.html', {'graph': image_data})


# monitoring/views.py
from django.shortcuts import render
from .models import Loss
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_losses(request):
    # Собираем данные о потерях (включая связанные данные о температуре и давлении)
    loss_data = Loss.objects.all().select_related('storage').values(
        'timestamp', 'quantity', 'storage__temperature', 'storage__pressure'
    )

    # Преобразуем данные в DataFrame
    df = pd.DataFrame(loss_data)

    # Убедимся, что данные существуют, прежде чем продолжить
    if df.empty:
        return render(request, 'monitoring/loss_prediction.html', {'error': 'Нет данных для прогнозирования.'})

    # Преобразуем данные для модели
    X = df[['storage__temperature', 'storage__pressure']]  # Признаки
    y = df['quantity']  # Целевая переменная

    # Обучаем модель
    model = LinearRegression()
    model.fit(X, y)

    # Прогнозируем потери
    df['predicted_loss'] = model.predict(X)

    # Передаем данные в шаблон для отображения
    return render(request, 'monitoring/loss_prediction.html', {'data': df.to_dict('records')})
