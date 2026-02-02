# curriculum/context_processors.py
from .models import DatosPersonales

def datos_personales_context(request):
    """Añade datos del perfil activo a todos los templates"""
    context = {}
    
    try:
        perfil_activo = DatosPersonales.objects.filter(perfilactivo=1).first()
        context['perfil_activo'] = perfil_activo
        
        if perfil_activo:
            context['config_pdf'] = {
                'experiencia': perfil_activo.imprimir_experiencia,
                'cursos': perfil_activo.imprimir_cursos,
                'reconocimientos': perfil_activo.imprimir_reconocimientos,
                'productos_academicos': perfil_activo.imprimir_productos_academicos,
                'productos_laborales': perfil_activo.imprimir_productos_laborales,
                'venta_garage': perfil_activo.imprimir_venta_garage,
            }
    except:
        # En caso de error (ej: migraciones pendientes)
        pass
    
    return context