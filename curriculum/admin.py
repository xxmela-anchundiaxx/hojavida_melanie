# curriculum/admin.py
from django.contrib import admin
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('idperfil', 'nombres', 'apellidos', 'numerocedula', 'perfilactivo')
    list_filter = ('perfilactivo', 'sexo')
    search_fields = ('nombres', 'apellidos', 'numerocedula')

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('idexperiencialaboral', 'cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'fechainiciogestion')
    search_fields = ('cargodesempenado', 'nombrempresa')

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('idreconocimiento', 'tiporeconocimiento', 'fechareconocimiento', 'activarparaqueseveaenfront')
    list_filter = ('tiporeconocimiento', 'activarparaqueseveaenfront')
    search_fields = ('descripcionreconocimiento',)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('idcursorealizado', 'nombrecurso', 'fechainicio', 'totalhoras', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'fechainicio')
    search_fields = ('nombrecurso', 'entidadpatrocinadora')

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('idproductoacademico', 'nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront',)
    search_fields = ('nombrerecurso', 'clasificador')

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('idproductoslaborales', 'nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'fechaproducto')
    search_fields = ('nombreproducto',)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('idventagarage', 'nombreproducto', 'estadoproducto', 'valordelbien', 'activarparaqueseveaenfront')
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')
    search_fields = ('nombreproducto',)