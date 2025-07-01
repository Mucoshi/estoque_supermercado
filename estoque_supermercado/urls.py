from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from estoque import views as estoque_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', include('estoque.urls')),  # Inclui as URLs do app 'estoque'
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cadastro/', estoque_views.cadastrar_usuario, name='cadastro'),
    path('', include('estoque.urls')),
    path('', estoque_views.listar_produtos, name='listar_produtos'),
    path('cadastro/sucesso/', estoque_views.cadastro_sucesso, name='cadastro_sucesso'),
    path('logout/', estoque_views.logout_view, name='logout'),
]


