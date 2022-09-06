from http.client import HTTPResponse
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
# Create your views here.

# def index(request):
#     return redirect('/agenda/') função para redirecionar o localhost para agenda
def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválidos")

    return redirect('/')


@login_required(login_url='/login/') # leve o usuário para página de login se ele não estiver logado
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1) # timedelta exibi as datas que vencidas com até 1 hora
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt = data_atual) # (__gt trás apenas os eventos que não aconteceram, __lt tras apenas os eventos de datas que já aconteceram)filtra os agendamentos por usuário
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados ['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento, descricao=descricao) outra forma de update
        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario)

    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento) # validação para apenas o usuário que estiver logado conseguir excluir apenas seus agendamentos
    except  Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(evento), safe=False)
