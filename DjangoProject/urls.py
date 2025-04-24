from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Стандартну адмінку прибираємо, якщо вона більше не потрібна
    # path('admin/', admin.site.urls),

    # Усі маршрути твого застосунку
    path('', include('Journal.urls')),
]
