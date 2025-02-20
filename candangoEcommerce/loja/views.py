from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Produto
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
