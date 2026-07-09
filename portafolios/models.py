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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['activo', 'fecha'], name='unique_precio_activo_fecha'),
        ]

class Weight(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=6)
    # No le pongo fecha porque los weights son solo para t=0

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['portafolio', 'activo'], name='unique_weight_portafolio_activo'),
        ]

class Cantidad(models.Model):
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['portafolio', 'activo'], name='unique_cantidad_portafolio_activo'),
        ]