from django.db import models

class Activo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Portafolio(models.Model):
    nombre = models.CharField(max_length=100)
    valor_inicial = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.nombre

class Precio(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    fecha = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=6)

class Weight(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=6)
    # No le pongo fecha porque los weights son solo para t=0

class Cantidad(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=20, decimal_places=6)