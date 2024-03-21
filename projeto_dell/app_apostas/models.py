from django.db import models

class Aposta(models.Model):
    id_aposta = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    cpf = models.CharField(max_length=14)  
    numero_1 = models.IntegerField()
    numero_2 = models.IntegerField()
    numero_3 = models.IntegerField()
    numero_4 = models.IntegerField()
    numero_5 = models.IntegerField()
    valor_premio = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.id_aposta:
            ultimo_id = Aposta.objects.order_by('-id_aposta').first()
            if ultimo_id:
                ultimo_id_aposta = ultimo_id.id_aposta
            else:
                ultimo_id_aposta = 999  # Defina o valor inicial
            self.id_aposta = ultimo_id_aposta + 1
        super(Aposta, self).save(*args, **kwargs)

class Sorteio(models.Model):
    id_sorteio = models.AutoField(primary_key=True)
    numero_sorteado = models.TextField(max_length=550)
    ganhador = models.TextField()
    rodadas = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Premio(models.Model):
    premio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    