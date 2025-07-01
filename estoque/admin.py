from django.contrib import admin
from .models import Produto

admin.site.register(Produto)

admin.site.site_header = "Administração do Sistema"
admin.site.site_title = "Administração do Sistema"
admin.site.index_title = "Painel de Controle"