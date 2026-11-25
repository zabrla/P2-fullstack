const elemento = document.getElementById('dados-mes');
if (elemento) {
    const dados = JSON.parse(elemento.textContent);
    new Chart(document.getElementById('graf'), {
        type: 'bar',
        data: {
            labels: dados.map(d => d.mes),
            datasets: [{
                label: 'Empréstimos por mês',
                data: dados.map(d => d.total),
            }]
        }
    });
}