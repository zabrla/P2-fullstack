from datetime import date
from django.db import models
from core.models import DaOrganizacao

class Autor(DaOrganizacao):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

class Livro(DaOrganizacao):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Exemplar(DaOrganizacao):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    codigo_registro = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.livro.titulo} - Cód: {self.codigo_registro}"

class Membro(DaOrganizacao):
    nome = models.CharField(max_length=150)
    email = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

class Emprestimo(DaOrganizacao):
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    data_emprestimo = models.DateField()
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(null=True, blank=True)

    @property
    def multa(self):
        referencia = self.data_devolucao_real or date.today()
        dias_atraso = (referencia - self.data_devolucao_prevista).days
        return max(0, dias_atraso) * 2.0

    def __str__(self):
        return f"Empréstimo: {self.exemplar.livro.titulo} para {self.membro.nome}"

class Reserva(DaOrganizacao):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    data_reserva = models.DateField()
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"Reserva: {self.livro.titulo} por {self.membro.nome}"