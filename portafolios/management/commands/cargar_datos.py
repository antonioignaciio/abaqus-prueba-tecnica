from django.core.management.base import BaseCommand
from portafolios.etl import cargar_datos

class Command(BaseCommand):
    help = "Carga los datos de activos, portafolios, weights y precios desde el Excel"

    def add_arguments(self, parser):
        parser.add_argument('ruta_archivo', type=str)

    def handle(self, *args, **options):
        ruta_archivo = options['ruta_archivo']
        cargar_datos(ruta_archivo)
        self.stdout.write(self.style.SUCCESS('Datos cargados correctamente'))