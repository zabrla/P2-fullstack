from datetime import date
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from .models import Livro, Exemplar, Emprestimo, Reserva

def kpis_gerais(org):
    metricas_emp = Emprestimo.objects.filter(organizacao=org).aggregate(
        total_emprestimos=Count('id'),
        emprestimos_ativos=Count('id', filter=Q(data_devolucao_real__isnull=True)),
        emprestimos_atrasados=Count(
            'id',
            filter=Q(data_devolucao_real__isnull=True, data_devolucao_prevista__lt=date.today()),
        ),
    )
    return {
        'total_livros': Livro.objects.filter(organizacao=org).count(),
        'exemplares_disponiveis': Exemplar.objects.filter(organizacao=org, disponivel=True).count(),
        'reservas_ativas': Reserva.objects.filter(organizacao=org, ativa=True).count(),
        **metricas_emp,
    }

def ranking_livros(org, limite=5):
    return list(
        Livro.objects.filter(organizacao=org)
        .annotate(total=Count('exemplar__emprestimo'))
        .order_by('-total')[:limite]
        .values('titulo', 'total')
    )

def emprestimos_por_mes(org):
    qs = (
        Emprestimo.objects.filter(organizacao=org)
        .annotate(mes=TruncMonth('data_emprestimo'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    return [
        {'mes': item['mes'].strftime('%Y-%m'), 'total': item['total']}
        for item in qs
        if item['mes']
    ]