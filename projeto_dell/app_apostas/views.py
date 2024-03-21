from django.shortcuts import render
from .models import Aposta, Sorteio, Premio
from collections import Counter
from decimal import Decimal
from django.db import connection

import random

def home(request):
    return render(request, 'home/home.html')


def apostas(request):
    if request.method == 'POST':
        nova_aposta = Aposta() 
        nova_aposta.nome = request.POST.get('nome')
        nova_aposta.cpf = request.POST.get('cpf')
        nova_aposta.numero_1 = request.POST.get('aposta_usuario1')
        nova_aposta.numero_2 = request.POST.get('aposta_usuario2')
        nova_aposta.numero_3 = request.POST.get('aposta_usuario3')
        nova_aposta.numero_4 = request.POST.get('aposta_usuario4')
        nova_aposta.numero_5 = request.POST.get('aposta_usuario5')
        nova_aposta.valor_premio = 0    
        
        nova_aposta.save()

    apostas = {
        'apostas': Aposta.objects.all()
    }
               
    return render(request, 'apostas/aposta.html', apostas)

    

def gerar_numeros():
    numeros_sorteados = random.sample(range(1, 51), 5)
    numeros_sorteados.sort() 
    # return '1, 3, 5, 6, 10'
    return numeros_sorteados

def gerar_numero_ultimo():
    
    
    numero = random.randint(1, 50)
    
    while True:
        ultimo_sorteio = Sorteio.objects.latest('id_sorteio')
        numeros_anteriores = ultimo_sorteio.numero_sorteado
        
        numeros_anteriores = ultimo_sorteio.numero_sorteado.strip('[]').split(', ')
        numeros_anteriores = [int(elem) for elem in numeros_anteriores]
        
        if numero in numeros_anteriores:
            numero = random.randint(1, 50)
        else:
            numeros_anteriores.append(numero)
            break
   
    return numeros_anteriores

    
def sorteios(request):
    if request.method == 'POST':
        novo_sorteio = Sorteio()
        novo_sorteio.numero_sorteado = gerar_numeros()
        novo_sorteio.ganhador = '--'
        
           
        novo_sorteio.valor = verificar_valor_premio()
        novo_sorteio.save()
    
    sorteios = {
        'sorteios': Sorteio.objects.all()
    }

    # Renderizando o template com as informações das apostas vencedoras
    return render(request, 'sorteios/sorteio.html', sorteios)

def verificar_valor_premio():  
    try:
        valor_premio = Premio.objects.latest('id')
    except Premio.DoesNotExist:
        valor_premio = Premio.objects.create(premio=gerar_valor_em_reais())
    else:
        valor_premio.premio += Decimal(str(gerar_valor_em_reais()))
        valor_premio.save()
    return valor_premio.premio

def apuracoes(request):
    
    ganhadores = []
    count = 0
    count_giros = 0
    count_apostas = 0
    valida = 0
    
    apostas = Aposta.objects.all()
    
    try:
        ultimo_sorteio = Sorteio.objects.latest('id_sorteio')
        valor = Premio.objects.latest('id')
    except Sorteio.DoesNotExist:
        ultimo_sorteio = None
        valor = None

    if request.method == 'POST':

        numeros_sorteio = ultimo_sorteio.numero_sorteado.strip('[]').split(', ')
        numeros_sorteio = [int(numero) for numero in numeros_sorteio]
        
        for aposta in apostas:
            numeros_apostados = [aposta.numero_1, aposta.numero_2, aposta.numero_3, aposta.numero_4, aposta.numero_5]
            count += 1
            if set(numeros_apostados).issubset(numeros_sorteio):
                ganhadores.append(aposta.cpf)
                
        if count == len(apostas) and len(ganhadores) == 0:
            for i in range(25):
                count_giros += 1
                
                ultimo = gerar_numero_ultimo()
                
                ultimo_sorteio.numero_sorteado = ultimo

                # ultimo_sorteio.numero_sorteado.sort()
                
                ultimo_sorteio.save()
                for aposta in apostas:
                    numeros_apostados = [aposta.numero_1, aposta.numero_2, aposta.numero_3, aposta.numero_4, aposta.numero_5]
                    
                    if set(numeros_apostados).issubset(ultimo):
                        ganhadores.append(aposta.cpf)
                        aposta.valor_premio = ultimo_sorteio.valor
                        valida = 1
                valor_premio = Premio.objects.latest('id')
                if ganhadores:
                    valor_premio.valor = 0.00
                
                if valida == 1:
                    break  
             
        ultimo_sorteio.ganhador = ganhadores
        ultimo_sorteio.rodadas = count_giros
        aposta.save()
        ultimo_sorteio.save()

    lista_numeros_apostados = numeros_apostados_com_frequencia(apostas)


    Apostas_sorteios = {
        'apostas': Aposta.objects.all(),
        'sorteios_ultimo': ultimo_sorteio,
        'sorteios_geral': Sorteio.objects.all(),
        'ganhadores_def': ganhadores,
        'apostas_ordenadas': Aposta.objects.all().order_by('nome'),
        'numeros_apostados': lista_numeros_apostados,
        'valor_premio': valor
    }
    
    return render(request, 'apuracoes/apuracao.html', Apostas_sorteios)

def numeros_apostados_com_frequencia(apostas):
    numeros_apostados = []

    for aposta in apostas:
        numeros_apostados.extend([
            aposta.numero_1,
            aposta.numero_2,
            aposta.numero_3,
            aposta.numero_4,
            aposta.numero_5
        ])

    frequencia_numeros = Counter(numeros_apostados)

    numeros_ordenados = sorted(frequencia_numeros.items(), key=lambda x: x[1], reverse=True)

    return numeros_ordenados

def gerar_valor_em_reais():
    return round(random.uniform(1, 100), 2)

def apagar_dados(request):
    # Apagar todos os objetos do modelo
    Aposta.objects.all().delete()
    Sorteio.objects.all().delete()
    Premio.objects.all().delete()
   
    return render(request, 'confirmacao/confirmacao_edicao.html')

