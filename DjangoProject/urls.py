from django.contrib import admin
from django.urls import path, include  # <- важливо

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Journal.urls')),  # <- ДОДАЙ ЦЕ, якщо немає!
]
