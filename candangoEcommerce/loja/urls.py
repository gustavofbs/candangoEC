from django.urls import path
from .views import lista_produtos, login_view, logout_view, adicionar_produto, editar_produto, excluir_produto

urlpatterns = [
    path("", lista_produtos, name="lista_produtos"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("adicionar/", adicionar_produto, name="adicionar_produto"),
    path("editar/<int:produto_id>/", editar_produto, name="editar_produto"),
    path("excluir/<int:produto_id>/", excluir_produto, name="excluir_produto"),
]

