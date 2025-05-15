from .models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, Presenca
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import calendar
from django.contrib import messages
from .models import Usuario
from django.utils import timezone
from datetime import datetime
import re



# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "index.html")

# usuarios/views.py


def is_senha_forte(senha):
    return (
        len(senha) >= 8 and
        re.search(r'[A-Z]', senha) and
        re.search(r'[a-z]', senha) and
        re.search(r'\d', senha) and
        re.search(r'[@$!%*?&#]', senha)
    )

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        password = request.POST.get('password')
        genero = request.POST.get('genero')
        data_nascimento = request.POST.get('data_nascimento')
        time = request.POST.get('time')

        # Validação do username
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return redirect('cadastro')
        if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
            messages.error(request, 'Nome de usuário inválido. Use apenas letras, números e _ . -')
            return redirect('cadastro')

        # Validação da data de nascimento
       
        try:
            nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
            if nascimento >= timezone.now().date():
                messages.error(request, 'Data de nascimento inválida.')
                return redirect('cadastro')
        except (ValueError, TypeError):
            messages.error(request, 'Formato de data inválido.')
            return redirect('cadastro')

        # Validação de senha forte
        if not is_senha_forte(password):
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres, incluindo maiúsculas, minúsculas, números e símbolos.')
            return redirect('cadastro')

        # Divisão do nome
        nome_split = nome.split()
        first_name = nome_split[0]
        last_name = ' '.join(nome_split[1:]) if len(nome_split) > 1 else ''

        # Criação do usuário
        Usuario.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            genero=genero,
            data_nascimento=nascimento,
            time=time,
            telefone=telefone,
            is_adolescente=True,
            is_lider=False
        )

        messages.success(request, 'Cadastro realizado com sucesso. Faça o login!')
        return redirect('login')

    return render(request, 'cadastro.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Usuario.objects.get(username=username)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                if user.is_lider:
                    return redirect('dashboard')
                else:
                    return redirect('dashboard')
            else:
                error = "Email ou senha inválidos."
        except Usuario.DoesNotExist:
            error = "Usuário não encontrado."
        
        return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def dashboard(request):
    eventos = Evento.objects.all()
    if not request.user.is_lider:
        return redirect('dashboard_adolescente')
    else:
        return render(request, 'dashboard-lider.html', {'eventos': eventos})

import calendar
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from .models import Evento, Presenca

def dashboard_adolescente(request):
    hoje = timezone.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())  # Segunda-feira
    fim_semana = inicio_semana + timedelta(days=6)         # Domingo

    # Lista de dias da semana usados para exibir corretamente em português
    dias_semana_pt = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    dias_chave = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']

    # Eventos únicos desta semana (por data)
    eventos_unicos = Evento.objects.filter(
        eh_periodico=False,
        data__range=(inicio_semana, fim_semana)
    )

    # Eventos periódicos cujo dia da semana está dentro da semana atual
    dias_futuros = dias_chave  # semana inteira
    eventos_periodicos = Evento.objects.filter(
        eh_periodico=True,
        dia_semana__in=dias_futuros
    )

    # Presenças do adolescente
    presencas = Presenca.objects.filter(adolescente=request.user)
    presenca_map = {p.evento_id: p.status for p in presencas}

    eventos_por_dia = {dia: [] for dia in dias_semana_pt}

    # Adiciona eventos únicos
    for evento in eventos_unicos:
        nome_dia = dias_semana_pt[evento.data.weekday()]
        eventos_por_dia[nome_dia].append({
            'id': evento.id,
            'nome': evento.nome,
            'local': evento.local,
            'horario': evento.horario.strftime('%H:%M'),
            'passado': evento.data < hoje,
            'presenca': presenca_map.get(evento.id)
        })

    # Adiciona eventos periódicos
    for evento in eventos_periodicos:
        index_dia = dias_chave.index(evento.dia_semana)
        data_evento = inicio_semana + timedelta(days=index_dia)
        nome_dia = dias_semana_pt[index_dia]
        eventos_por_dia[nome_dia].append({
            'id': evento.id,
            'nome': evento.nome,
            'local': evento.local,
            'horario': evento.horario.strftime('%H:%M'),
            'passado': data_evento < hoje,
            'presenca': presenca_map.get(evento.id)
        })

    return render(request, 'dashboard.html', {
        'eventos_por_dia': eventos_por_dia
    })

@login_required
def registrar_presenca(request, evento_id, status):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST' and status in ['sim', 'nao']:
        presenca, created = Presenca.objects.update_or_create(
            adolescente=request.user,
            evento=evento,
            defaults={'status': status}
        )
    return redirect('dashboard_adolescente')

@login_required
def criar_evento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        eh_periodico = request.POST.get('eh_periodico')
        horario = request.POST.get('horario')
        local = request.POST.get('local')
        print(eh_periodico)

        if eh_periodico:
            dia_semana = request.POST.get('dia_semana')
            evento = Evento.objects.create(
                nome=nome,
                eh_periodico=True,
                dia_semana=dia_semana,
                horario=horario,
                local=local,
                criador=request.user
            )
        else:
            data = request.POST.get('data')
            evento = Evento.objects.create(
                nome=nome,
                eh_periodico=False,
                data=data,
                horario=horario,
                local=local,
                criador=request.user
            )

        return redirect('dashboard')

    return render(request, 'criar-evento.html')

def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        eh_periodico = request.POST.get('eh_periodico') == 'True'
        horario = request.POST.get('horario')
        local = request.POST.get('local')

        if eh_periodico:
            dia_semana = request.POST.get('dia_semana')
            evento.nome = nome
            evento.eh_periodico = True
            evento.dia_semana = dia_semana
            evento.horario = horario
            evento.local = local
        else:
            data = request.POST.get('data')
            evento.nome = nome
            evento.eh_periodico = False
            evento.data = data
            evento.horario = horario
            evento.local = local

        evento.save()
        return redirect('dashboard')

    return render(request, 'editar-evento.html', {'evento': evento})


def excluir_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    evento.delete()
    return redirect('dashboard')


