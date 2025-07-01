from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .forms import ProdutoForm
from django.db.models import Sum, Count
import openpyxl
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import json
from django.db.models import Sum
from django.utils.safestring import mark_safe
from django.db.models import Count, Q
from io import BytesIO
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db.models import F
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

@login_required
def listar_produtos(request):
    produtos = Produto.objects.all()
    baixo_estoque = produtos.filter(quantidade__lte=F('estoque_minimo'))
    qtd_baixo_estoque = baixo_estoque.count()

    return render(request, 'estoque/listar_produtos.html', {
        'produtos': produtos,
        'baixo_estoque': baixo_estoque,
        'qtd_baixo_estoque': qtd_baixo_estoque
    })

@login_required
@permission_required('estoque.adicionar_produto', raise_exception=True)
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'estoque/adicionar_produto.html', {'form': form})
produtos = Produto.objects.all()

@login_required
@login_required
@permission_required('estoque.change_produto', raise_exception=True)
def editar_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'estoque/editar_produto.html', {'form': form})
produtos = Produto.objects.all()

@login_required
@permission_required('estoque.delete_produto', raise_exception=True)
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    return render(request, 'estoque/excluir_produto.html', {'produto': produto})
produtos = Produto.objects.all()

@login_required
def dashboard(request):
    produtos = Produto.objects.all()

    categorias = ['alimentos', 'limpeza', 'vestuario', 'bazar']
    quantidades = [
        produtos.filter(categoria='alimentos').aggregate(Sum('quantidade'))['quantidade__sum'] or 0,
        produtos.filter(categoria='limpeza').aggregate(Sum('quantidade'))['quantidade__sum'] or 0,
        produtos.filter(categoria='vestuario').aggregate(Sum('quantidade'))['quantidade__sum'] or 0,
        produtos.filter(categoria='bazar').aggregate(Sum('quantidade'))['quantidade__sum'] or 0,
    ]

    nomes_produtos = list(produtos.values_list('nome', flat=True))
    quantidades_produtos = list(produtos.values_list('quantidade', flat=True))

    baixo_estoque = produtos.filter(quantidade__lt=5)

    context = {
    'categorias': mark_safe(json.dumps(categorias)),
    'quantidades': mark_safe(json.dumps(quantidades)),
    'nomes_produtos': mark_safe(json.dumps(nomes_produtos)),
    'quantidades_produtos': mark_safe(json.dumps(quantidades_produtos)),
    'qtd_baixo_estoque': baixo_estoque.count(),
    'baixo_estoque': baixo_estoque,
}


    return render(request, 'estoque/dashboard.html', context)

@login_required
def exportar_excel(request):
    produtos = Produto.objects.all()

    # Criar workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Produtos"

    # Cabeçalho
    ws.append(["Nome", "Categoria", "Quantidade", "Preço", "Validade"])

    # Dados
    for produto in produtos:
        ws.append([
            produto.nome,
            produto.get_categoria_display(),
            produto.quantidade,
            float(produto.preco),
            produto.data_validade.strftime('%d/%m/%Y') if produto.data_validade else ''
        ])

    # Salvar para memória (BytesIO)
    arquivo = BytesIO()
    wb.save(arquivo)
    arquivo.seek(0)

    # Retornar como resposta HTTP
    response = HttpResponse(
        arquivo,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="produtos.xlsx"'
    return response
produtos = Produto.objects.all()

@login_required
def exportar_pdf(request):
    produtos = Produto.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="produtos.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(200, 820, "Lista de Produtos")

    y = 800
    for produto in produtos:
        linha = f"{produto.nome} | {produto.get_categoria_display()} | {produto.quantidade} | R$ {produto.preco}"
        p.drawString(50, y, linha)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response
produtos = Produto.objects.all()

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro_sucesso')
    else:
        form = UserCreationForm()
    return render(request, 'registration/cadastro.html', {'form': form})

def cadastro_sucesso(request):
    return render(request, 'registration/cadastro_sucesso.html')

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

def erro_403(request, exception=None):
    return render(request, '403.html', status=403)

LIMITE_ESTOQUE_BAIXO = 5
