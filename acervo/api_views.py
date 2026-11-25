from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils import org_atual
from .dashboard import kpis_gerais, ranking_livros, emprestimos_por_mes
from .models import Autor, Livro, Exemplar, Membro, Emprestimo, Reserva
from .serializers import (
    AutorSerializer,
    LivroSerializer,
    ExemplarSerializer,
    MembroSerializer,
    EmprestimoSerializer,
    ReservaSerializer,
)

class DaOrganizacaoMixin:
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(organizacao=org_atual(self.request))

    def perform_create(self, serializer):
        serializer.save(organizacao=org_atual(self.request))

class AutorListCreate(DaOrganizacaoMixin, generics.ListCreateAPIView):
    model = Autor
    serializer_class = AutorSerializer

class AutorRetrieveUpdateDestroy(DaOrganizacaoMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Autor
    serializer_class = AutorSerializer

class LivroListCreate(DaOrganizacaoMixin, generics.ListCreateAPIView):
    model = Livro
    serializer_class = LivroSerializer

class LivroRetrieveUpdateDestroy(DaOrganizacaoMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Livro
    serializer_class = LivroSerializer

class ExemplarListCreate(DaOrganizacaoMixin, generics.ListCreateAPIView):
    model = Exemplar
    serializer_class = ExemplarSerializer

class ExemplarRetrieveUpdateDestroy(DaOrganizacaoMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Exemplar
    serializer_class = ExemplarSerializer

class MembroListCreate(DaOrganizacaoMixin, generics.ListCreateAPIView):
    model = Membro
    serializer_class = MembroSerializer

class MembroRetrieveUpdateDestroy(DaOrganizacaoMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Membro
    serializer_class = MembroSerializer

class EmprestimoListCreate(DaOrganizacaoMixin, generics.ListCreateAPIView):
    model = Emprestimo
    serializer_class = EmprestimoSerializer

class EmprestimoRetrieveUpdateDestroy(DaOrganizacaoMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Emprestimo
    serializer_class = EmprestimoSerializer

class ReservaListCreate(DaOrganizacaoMixin, generics.ListCreateAPIView):
    model = Reserva
    serializer_class = ReservaSerializer

class ReservaRetrieveUpdateDestroy(DaOrganizacaoMixin, generics.RetrieveUpdateDestroyAPIView):
    model = Reserva
    serializer_class = ReservaSerializer

class DashboardApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        org = org_atual(request)
        eh_admin = request.user.perfil.papel == 'admin'
        dados = {
            'kpis': kpis_gerais(org),
            'ranking': ranking_livros(org),
        }
        if eh_admin:
            dados['por_mes'] = emprestimos_por_mes(org)
        return Response(dados)