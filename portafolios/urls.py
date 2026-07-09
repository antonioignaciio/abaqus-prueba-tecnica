from django.urls import path, include
from portafolios.views import EvolucionPortafolioView, vista_evolucion_portafolio

urlpatterns = [
    path('portafolios/<int:portafolio_id>/evolucion/', EvolucionPortafolioView.as_view(), name='evolucion-portafolio'),
    path('portafolios/<int:portafolio_id>/', vista_evolucion_portafolio, name='vista-evolucion-portafolio')
]