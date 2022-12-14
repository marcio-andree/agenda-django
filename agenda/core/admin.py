from django.contrib import admin
from core.models import Evento #tem que importar os models e registra los

# Register your models here.
class EventoAdmin(admin.ModelAdmin):
  list_display = ('id','titulo','descricao','data_evento','data_criacao')
  list_filter = ('usuario',) # Adiciona filtro por titulo da classe evento

admin.site.register(Evento, EventoAdmin)
