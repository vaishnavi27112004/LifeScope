from django.urls import path
from . import views

app_name = "tracker"

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_data, name='add_data'),
    path('history/', views.history, name='history'),
    path('predict/', views.predict, name='predict'),
]




