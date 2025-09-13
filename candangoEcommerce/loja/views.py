from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Produto, ItemCarrinho
from .forms import ProdutoForm  # Importando o formulário que vamos criar

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "loja/lista_produtos.html", {"produtos": produtos})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("lista_produtos")
    return render(request, "loja/login.html")

def logout_view(request):
    logout(request)
    return redirect("lista_produtos")

@login_required
def adicionar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_produtos")
    else:
        form = ProdutoForm()
    return render(request, "loja/adicionar_produto.html", {"form": form})

@login_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect("lista_produtos")
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "loja/editar_produto.html", {"form": form, "produto": produto})

@login_required
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == "POST":
        produto.delete()
        return redirect("lista_produtos")
    return render(request, "loja/excluir_produto.html", {"produto": produto})

# Funções do Carrinho de Compras

def _get_session_key(request):
    """Garante que a sessão existe e retorna a chave da sessão"""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _atualizar_contagem_carrinho(request):
    """Atualiza a contagem de itens no carrinho na sessão"""
    session_key = _get_session_key(request)
    count = ItemCarrinho.objects.filter(session_key=session_key).count()
    request.session['cart_count'] = count
    return count

def visualizar_carrinho(request):
    """Exibe o carrinho de compras"""
    session_key = _get_session_key(request)
    itens = ItemCarrinho.objects.filter(session_key=session_key)
    
    total = sum(item.subtotal() for item in itens)
    _atualizar_contagem_carrinho(request)
    
    return render(request, "loja/carrinho.html", {
        "itens": itens,
        "total": total
    })

@require_POST
def adicionar_ao_carrinho(request, produto_id):
    """Adiciona um produto ao carrinho ou incrementa sua quantidade"""
    produto = get_object_or_404(Produto, id=produto_id)
    session_key = _get_session_key(request)
    quantidade = int(request.POST.get('quantidade', 1))
    
    # Tenta obter o item ou cria um novo
    item, created = ItemCarrinho.objects.get_or_create(
        session_key=session_key,
        produto=produto,
        defaults={'quantidade': quantidade}
    )
    
    # Se o item já existia, incrementa a quantidade
    if not created:
        item.quantidade += quantidade
        item.save()
    
    # Atualiza a contagem de itens no carrinho na sessão
    cart_count = _atualizar_contagem_carrinho(request)
    
    messages.success(request, f"{produto.nome} adicionado ao carrinho!")
    
    # Verifica se a requisição é AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f"{produto.nome} adicionado ao carrinho!",
            'cart_count': cart_count
        })
    
    # Redireciona de volta para a página anterior ou para a lista de produtos
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('lista_produtos')

@require_POST
def atualizar_carrinho(request, item_id):
    """Atualiza a quantidade de um item no carrinho"""
    item = get_object_or_404(ItemCarrinho, id=item_id, session_key=_get_session_key(request))
    quantidade = int(request.POST.get('quantidade', 1))
    
    if quantidade > 0:
        item.quantidade = quantidade
        item.save()
        messages.success(request, "Carrinho atualizado!")
    else:
        item.delete()
        messages.success(request, "Item removido do carrinho!")
    
    # Atualiza a contagem de itens no carrinho na sessão
    _atualizar_contagem_carrinho(request)
    
    return redirect('visualizar_carrinho')

@require_POST
def remover_do_carrinho(request, item_id):
    """Remove um item do carrinho"""
    item = get_object_or_404(ItemCarrinho, id=item_id, session_key=_get_session_key(request))
    produto_nome = item.produto.nome
    item.delete()
    
    # Atualiza a contagem de itens no carrinho na sessão
    _atualizar_contagem_carrinho(request)
    
    messages.success(request, f"{produto_nome} removido do carrinho!")
    return redirect('visualizar_carrinho')

def limpar_carrinho(request):
    """Remove todos os itens do carrinho"""
    session_key = _get_session_key(request)
    ItemCarrinho.objects.filter(session_key=session_key).delete()
    
    # Atualiza a contagem de itens no carrinho na sessão
    _atualizar_contagem_carrinho(request)
    
    messages.success(request, "Carrinho esvaziado!")
    return redirect('visualizar_carrinho')
