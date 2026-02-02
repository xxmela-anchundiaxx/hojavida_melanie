# curriculum/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from datetime import date

from .models import *

def hoja_de_vida(request):
    """
    Vista única para la hoja de vida pública.
    Muestra el perfil activo si existe, o una página de bienvenida.
    """
    # Obtener perfil activo
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    context = {
        'perfil': perfil,
        'hoy': date.today(),
    }
    
    # Si hay perfil activo, cargar sus datos
    if perfil:
        # Solo cargar datos si están configurados para mostrar
        if perfil.mostrar_experiencia:
            context['experiencias'] = perfil.experiencias.filter(
                activarparaqueseveaenfront=True
            ).order_by('-fechainiciogestion')
        
        if perfil.mostrar_cursos:
            context['cursos'] = perfil.cursos.filter(
                activarparaqueseveaenfront=True
            ).order_by('-fechainicio')
        
        if perfil.mostrar_reconocimientos:
            context['reconocimientos'] = perfil.reconocimientos.filter(
                activarparaqueseveaenfront=True
            ).order_by('-fechareconocimiento')
        
        if perfil.mostrar_productos_academicos:
            context['productos_academicos'] = perfil.productos_academicos.filter(
                activarparaqueseveaenfront=True
            ).order_by('-fecha_registro')
        
        if perfil.mostrar_productos_laborales:
            context['productos_laborales'] = perfil.productos_laborales.filter(
                activarparaqueseveaenfront=True
            ).order_by('-fechaproducto')
        
        if perfil.mostrar_venta_garage:
            context['ventas_garage'] = perfil.ventas_garage.filter(
                activarparaqueseveaenfront=True
            ).order_by('-fecha_publicacion')
    
    return render(request, 'curriculum/hoja_de_vida.html', context)


# =============================================================================
# FUNCIONES PARA OBTENER DATOS (usado por todas las opciones de PDF)
# =============================================================================

def obtener_datos_para_pdf(perfil):
    """Función auxiliar para obtener todos los datos necesarios para el PDF"""
    context = {
        'perfil': perfil,
        'hoy': date.today(),
        'es_pdf': True,
    }
    
    if perfil.imprimir_experiencia:
        context['experiencias'] = perfil.experiencias.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fechainiciogestion')
    
    if perfil.imprimir_cursos:
        context['cursos'] = perfil.cursos.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fechainicio')
    
    if perfil.imprimir_reconocimientos:
        context['reconocimientos'] = perfil.reconocimientos.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fechareconocimiento')
    
    if perfil.imprimir_productos_academicos:
        context['productos_academicos'] = perfil.productos_academicos.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fecha_registro')
    
    if perfil.imprimir_productos_laborales:
        context['productos_laborales'] = perfil.productos_laborales.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fechaproducto')
    
    if perfil.imprimir_venta_garage:
        context['ventas_garage'] = perfil.ventas_garage.filter(
            activarparaqueseveaenfront=True
        ).order_by('-fecha_publicacion')
    
    return context


# =============================================================================
# OPCIÓN 1: HTML PARA IMPRIMIR (MÁS SIMPLE - NO REQUIERE INSTALACIÓN)
# Esta es la opción actual y más simple. El usuario presiona Ctrl+P
# =============================================================================

def generar_pdf(request):
    """
    OPCIÓN 1: HTML para imprimir (ACTUAL)
    Genera una página HTML optimizada para que el usuario imprima a PDF.
    Permite recibir parámetros en la petición (GET) para indicar qué
    secciones incluir sin modificar las preferencias guardadas en el modelo.
    Parámetros esperados (valores: '1' = incluir, '0' = excluir):
      - incluir_experiencia
      - incluir_cursos
      - incluir_reconocimientos
      - incluir_productos_academicos
      - incluir_productos_laborales
      - incluir_venta_garage
    """
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()

    if not perfil:
        return redirect('hoja_de_vida')

    params = request.GET
    # Si no hay parámetros 'incluir_' => usar flags guardados
    if not any(k.startswith('incluir_') for k in params.keys()):
        context = obtener_datos_para_pdf(perfil)
        return render(request, 'curriculum/pdf_template.html', context)

    context = {
        'perfil': perfil,
        'hoy': date.today(),
        'es_pdf': True,
    }

    def param_bool(name, default=False):
        val = params.get(name)
        if val is None:
            return default
        return val in ['1', 'true', 'True', 'on']

    if param_bool('incluir_experiencia'):
        context['experiencias'] = perfil.experiencias.filter(activarparaqueseveaenfront=True).order_by('-fechainiciogestion')

    if param_bool('incluir_cursos'):
        context['cursos'] = perfil.cursos.filter(activarparaqueseveaenfront=True).order_by('-fechainicio')

    if param_bool('incluir_reconocimientos'):
        context['reconocimientos'] = perfil.reconocimientos.filter(activarparaqueseveaenfront=True).order_by('-fechareconocimiento')

    if param_bool('incluir_productos_academicos'):
        context['productos_academicos'] = perfil.productos_academicos.filter(activarparaqueseveaenfront=True).order_by('-fecha_registro')

    if param_bool('incluir_productos_laborales'):
        context['productos_laborales'] = perfil.productos_laborales.filter(activarparaqueseveaenfront=True).order_by('-fechaproducto')

    if param_bool('incluir_venta_garage'):
        context['ventas_garage'] = perfil.ventas_garage.filter(activarparaqueseveaenfront=True).order_by('-fecha_publicacion')

    return render(request, 'curriculum/pdf_template.html', context)


# =============================================================================
# OPCIÓN 2: WEASYPRINT (PDF AUTOMÁTICO - REQUIERE INSTALACIÓN)
# Descomenta esta función y comenta la anterior para usar WeasyPrint
# Instalación: pip install weasyprint
# =============================================================================

"""
def generar_pdf(request):
    '''
    OPCIÓN 2: WeasyPrint (PDF AUTOMÁTICO)
    Genera y descarga un PDF real automáticamente
    
    REQUISITOS:
    1. pip install weasyprint
    2. En Windows: Instalar GTK3 (ver GUIA_CLOUDINARY_Y_PDF.md)
    '''
    try:
        from weasyprint import HTML
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        # Si WeasyPrint no está instalado, usar opción HTML
        return generar_pdf_html(request)
    
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if not perfil:
        return redirect('hoja_de_vida')
    
    context = obtener_datos_para_pdf(perfil)
    
    # Renderizar el template HTML
    html_string = render_to_string('curriculum/pdf_template.html', context)
    
    # Configurar fuentes
    font_config = FontConfiguration()
    
    # Convertir HTML a PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf(font_config=font_config)
    
    # Crear respuesta HTTP con el PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{perfil.nombres}_{perfil.apellidos}.pdf"'
    
    return response
"""


# =============================================================================
# OPCIÓN 3: REPORTLAB (PDF PERSONALIZADO - REQUIERE MÁS CÓDIGO)
# Descomenta esta función para usar ReportLab
# Instalación: pip install reportlab
# =============================================================================

"""
def generar_pdf(request):
    '''
    OPCIÓN 3: ReportLab (PDF PERSONALIZADO)
    Genera un PDF desde cero con ReportLab
    
    REQUISITOS:
    1. pip install reportlab
    '''
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib import colors
    from io import BytesIO
    
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if not perfil:
        return redirect('hoja_de_vida')
    
    context = obtener_datos_para_pdf(perfil)
    
    # Crear buffer para el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    # Título con nombre completo
    nombre_completo = f"{perfil.nombres} {perfil.apellidos}"
    story.append(Paragraph(nombre_completo, titulo_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Datos personales
    if perfil.descripcionperfil:
        story.append(Paragraph(perfil.descripcionperfil, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    if perfil.numerocedula:
        story.append(Paragraph(f"<b>Cédula:</b> {perfil.numerocedula}", styles['Normal']))
    if perfil.telefonoconvencional:
        story.append(Paragraph(f"<b>Teléfono:</b> {perfil.telefonoconvencional}", styles['Normal']))
    if perfil.direcciondomiciliaria:
        story.append(Paragraph(f"<b>Dirección:</b> {perfil.direcciondomiciliaria}", styles['Normal']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Experiencia Laboral
    experiencias = context.get('experiencias')
    if experiencias:
        story.append(Paragraph("EXPERIENCIA LABORAL", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        for exp in experiencias:
            fecha_fin = exp.fechafingestion.strftime("%m/%Y") if exp.fechafingestion else "Presente"
            fecha_inicio = exp.fechainiciogestion.strftime("%m/%Y")
            
            story.append(Paragraph(f"<b>{exp.cargodesempenado}</b>", styles['Heading3']))
            story.append(Paragraph(f"{exp.nombrempresa} | {fecha_inicio} - {fecha_fin}", styles['Normal']))
            if exp.descripcionfunciones:
                story.append(Paragraph(exp.descripcionfunciones, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    # Cursos
    cursos = context.get('cursos')
    if cursos:
        story.append(Paragraph("FORMACIÓN Y CURSOS", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        for curso in cursos:
            fecha_inicio = curso.fechainicio.strftime("%m/%Y")
            fecha_fin = curso.fechafin.strftime("%m/%Y") if curso.fechafin else "Presente"
            
            story.append(Paragraph(f"<b>{curso.nombrecurso}</b>", styles['Heading3']))
            story.append(Paragraph(f"{curso.entidadpatrocinadora} | {fecha_inicio} - {fecha_fin}", styles['Normal']))
            if curso.totalhoras:
                story.append(Paragraph(f"Duración: {curso.totalhoras} horas", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
    
    # Construir PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    
    # Crear respuesta HTTP con el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{perfil.nombres}_{perfil.apellidos}.pdf"'
    
    return response
"""


# =============================================================================
# API - DATOS PERSONALES
# =============================================================================

def api_datos_personales(request):
    """API para obtener datos personales"""
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    
    if not perfil:
        return JsonResponse({'error': 'No hay perfil disponible'}, status=404)
    
    data = {
        'nombres': perfil.nombres,
        'apellidos': perfil.apellidos,
        'descripcion': perfil.descripcionperfil,
        'foto': perfil.foto_perfil.url if perfil.foto_perfil else None,
        'cedula': perfil.numerocedula,
        'telefono': perfil.telefonoconvencional,
        'direccion': perfil.direcciondomiciliaria,
        'web': perfil.sitioweb,
    }
    
    return JsonResponse(data)


