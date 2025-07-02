# Define as rotas da aplicação que conectam URLs às funções nas views.
from django.urls import path
from . import views

urlpatterns = [
# Define as rotas da aplicação que conectam URLs às funções nas views.
# Rota principal que mostra os produtos em estoque.
    path('', views.listar_produtos, name='listar_produtos'),
# Define as rotas da aplicação que conectam URLs às funções nas views.
    path('dashboard/', views.dashboard, name='dashboard'),
# Define as rotas da aplicação que conectam URLs às funções nas views.
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
# Define as rotas da aplicação que conectam URLs às funções nas views.
    path('editar/<int:id>/', views.editar_produto, name='editar_produto'),
# Define as rotas da aplicação que conectam URLs às funções nas views.
    path('excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),
# Define as rotas da aplicação que conectam URLs às funções nas views.
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
# Define as rotas da aplicação que conectam URLs às funções nas views.
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
]

handler403 = 'estoque.views.erro_403'