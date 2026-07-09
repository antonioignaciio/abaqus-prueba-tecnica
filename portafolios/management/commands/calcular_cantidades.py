from django.core.management.base import BaseCommand
from portafolios.services import calcular_cantidades_iniciales


class Command(BaseCommand):
    help = "Calcula y guarda las cantidades iniciales (C_i0) a partir de los weights"

    def handle(self, *args, **options):
        calcular_cantidades_iniciales()
        self.stdout.write(self.style.SUCCESS('Cantidades iniciales calculadas correctamente'))