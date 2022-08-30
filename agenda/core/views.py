from django.shortcuts import render, redirect
from core.models import Evento
# Create your views here.

# def index(request):
#     return redirect('/agenda/') função para redirecionar o localhost para agenda

def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.all() # .filter(usuario=usuario) filtra os agendamentos por usuário
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

