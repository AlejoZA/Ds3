from django.urls import path
from .views import registro_usuario, actualizar_usuario, obtener_usuario, iniciar_sesion, cerrar_sesion

urlpatterns = [
    path('registro/', registro_usuario, name='registro_usuario'),
    path('usuario/<int:id_usuario>/', obtener_usuario, name='obtener_usuario'),
    path('usuario/<int:id_usuario>/actualizar/', actualizar_usuario, name='actualizar_usuario'),
    path('iniciar-sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),
]
    