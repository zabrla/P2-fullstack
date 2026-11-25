import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from core.utils import org_atual
from .dashboard import kpis_gerais, ranking_livros, emprestimos_por_mes
from .models import Emprestimo

def _limpar_celula_csv(valor):
    texto = str(valor)
    if texto and texto[0] in ('=', '+', '-', '@'):
        return f"'{texto}"
    return texto

@login_required
def dashboard(request):
    org = org_atual(request)
    eh_admin = request.user.perfil.papel == 'admin'
    contexto = {
        'organizacao': org,
        'eh_admin': eh_admin,
        'kpis': kpis_gerais(org),
        'ranking': ranking_livros(org),
        'por_mes': emprestimos_por_mes(org) if eh_admin else [],
    }
    return render(request, 'acervo/dashboard.html', contexto)

@login_required
def exportar_emprestimos_csv(request):
    if request.user.perfil.papel != 'admin':
        return HttpResponseForbidden('Acesso restrito a administradores.')

    org = org_atual(request)
    qs = (
        Emprestimo.objects.filter(organizacao=org)
        .select_related('exemplar__livro', 'membro')
        .order_by('-data_emprestimo')
    )

    resp = HttpResponse(content_type='text/csv; charset=utf-8')
    resp['Content-Disposition'] = 'attachment; filename="emprestimos.csv"'
    writer = csv.writer(resp)
    writer.writerow(['Livro', 'Exemplar', 'Membro', 'Data Empréstimo', 'Devolução Prevista', 'Devolução Real', 'Multa'])
    for e in qs:
        writer.writerow([
            _limpar_celula_csv(e.exemplar.livro.titulo),
            _limpar_celula_csv(e.exemplar.codigo_registro),
            _limpar_celula_csv(e.membro.nome),
            e.data_emprestimo,
            e.data_devolucao_prevista,
            e.data_devolucao_real or '',
            f"{e.multa:.2f}",
        ])
    return resp