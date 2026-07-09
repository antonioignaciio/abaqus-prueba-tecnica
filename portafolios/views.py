from datetime import date
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from portafolios.models import Portafolio
from portafolios.services import calcular_evolucion
from portafolios.serializers import EvolucionDiaSerializer

# Create your views here.

class EvolucionPortafolioView(APIView):
    def get(self, request, portafolio_id):
        portafolio = get_object_or_404(Portafolio, id=portafolio_id)

        fecha_inicio_str = request.query_params.get('fecha_inicio')
        fecha_fin_str = request.query_params.get('fecha_fin')

        if not fecha_inicio_str or not fecha_fin_str:
            return Response(
                {"error": "Debes indicar fecha_inicio y fecha_fin"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Las fechas deben tener el formato YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if fecha_inicio > fecha_fin:
            return Response(
                {"error": "fecha_inicio no puede ser posterior a fecha_fin"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        resultado = calcular_evolucion(portafolio, fecha_inicio, fecha_fin)
        serializer = EvolucionDiaSerializer(resultado, many=True)
        return Response(serializer.data)

def vista_evolucion_portafolio(request, portafolio_id):
    contexto = {
        'portafolio_id': portafolio_id
    }
    return render(request, 'portafolios/evolucion.html', contexto)