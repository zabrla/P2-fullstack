from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='inicio'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('relatorios/emprestimos.csv', views.exportar_emprestimos_csv, name='exportar-emprestimos-csv'),
]