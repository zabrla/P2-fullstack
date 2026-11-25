from django.urls import path
from . import api_views

urlpatterns = [
    path('autores/', api_views.AutorListCreate.as_view(), name='autor-list'),
    path('autores/<int:pk>/', api_views.AutorRetrieveUpdateDestroy.as_view(), name='autor-detail'),

    path('livros/', api_views.LivroListCreate.as_view(), name='livro-list'),
    path('livros/<int:pk>/', api_views.LivroRetrieveUpdateDestroy.as_view(), name='livro-detail'),

    path('exemplares/', api_views.ExemplarListCreate.as_view(), name='exemplar-list'),
    path('exemplares/<int:pk>/', api_views.ExemplarRetrieveUpdateDestroy.as_view(), name='exemplar-detail'),

    path('membros/', api_views.MembroListCreate.as_view(), name='membro-list'),
    path('membros/<int:pk>/', api_views.MembroRetrieveUpdateDestroy.as_view(), name='membro-detail'),

    path('emprestimos/', api_views.EmprestimoListCreate.as_view(), name='emprestimo-list'),
    path('emprestimos/<int:pk>/', api_views.EmprestimoRetrieveUpdateDestroy.as_view(), name='emprestimo-detail'),

    path('reservas/', api_views.ReservaListCreate.as_view(), name='reserva-list'),
    path('reservas/<int:pk>/', api_views.ReservaRetrieveUpdateDestroy.as_view(), name='reserva-detail'),

    path('dashboard/', api_views.DashboardApi.as_view(), name='api-dashboard'),
]