from django.urls import path
from app_apostas import views

urlpatterns = [
    # rota, view responsavel, nome da referencia
    path('', views.home, name='home'),
    # path('usuarios/', views.usuarios, name='listagem_usuarios'),
    path('apostas/', views.apostas, name='nova_aposta'),
    path('sorteio/', views.sorteios, name='sorteio'),
    path('apuracao/', views.apuracoes, name='apuracao'),
    path('apagar_dados/', views.apagar_dados, name='apagar_dados'),

]
