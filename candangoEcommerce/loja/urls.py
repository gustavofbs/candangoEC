from django.urls import path
from .views import (
    lista_produtos, login_view, logout_view, 
    adicionar_produto, editar_produto, excluir_produto,
    visualizar_carrinho, adicionar_ao_carrinho, atualizar_carrinho,
    remover_do_carrinho, limpar_carrinho
)

urlpatterns = [
    # URLs de produtos
    path("", lista_produtos, name="lista_produtos"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("adicionar/", adicionar_produto, name="adicionar_produto"),
    path("editar/<int:produto_id>/", editar_produto, name="editar_produto"),
    path("excluir/<int:produto_id>/", excluir_produto, name="excluir_produto"),
    
    # URLs do carrinho de compras
    path("carrinho/", visualizar_carrinho, name="visualizar_carrinho"),
    path("carrinho/adicionar/<int:produto_id>/", adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path("carrinho/atualizar/<int:item_id>/", atualizar_carrinho, name="atualizar_carrinho"),
    path("carrinho/remover/<int:item_id>/", remover_do_carrinho, name="remover_do_carrinho"),
    path("carrinho/limpar/", limpar_carrinho, name="limpar_carrinho"),
]
