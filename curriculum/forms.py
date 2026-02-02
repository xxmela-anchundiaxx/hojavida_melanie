from django import forms
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)

from django import forms
from .models import DatosPersonales

class SeleccionSeccionesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = [
            'imprimir_experiencia', 
            'imprimir_reconocimientos', 
            'imprimir_cursos', 
            'imprimir_productos_academicos',
            'imprimir_productos_laborales',
            'imprimir_venta_garage', 
        ]
        widgets = {
            'imprimir_experiencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_reconocimientos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_cursos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_productos_academicos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_productos_laborales': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imprimir_venta_garage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = [
            'foto_perfil',
            'descripcionperfil', 'nombres', 'apellidos', 'nacionalidad',
            'lugarnacimiento', 'fechanacimiento', 'numerocedula', 'sexo',
            'estadocivil', 'licenciaconducir', 'telefonoconvencional',
            'telefonofijo', 'direcciontrabajo', 'direcciondomiciliaria', 'sitioweb'
        ]
        widgets = {
            'fechanacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcionperfil': forms.TextInput(attrs={'placeholder': 'Ej: Desarrollador Full Stack', 'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'placeholder': 'Nombres completos', 'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellidos completos', 'class': 'form-control'}),
            # He añadido 'form-control' a los demás para que se vean bien con tu CSS
        }

    def __init__(self, *args, **kwargs):
        super(DatosPersonalesForm, self).__init__(*args, **kwargs)
        
        # Lógica de bloqueo para edición
        if self.instance and self.instance.pk:
            # Si el perfil ya existe en la base de datos (estamos editando)
            
            if self.instance.fechanacimiento:
                # Bloqueamos el campo en el HTML y el servidor lo ignorará si intentan cambiarlo
                self.fields['fechanacimiento'].disabled = True
                self.fields['fechanacimiento'].help_text = "Dato protegido: No se puede modificar."

            if self.instance.numerocedula:
                # Opcional: Bloqueamos también la cédula por seguridad
                self.fields['numerocedula'].disabled = True

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = [
            'cargodesempenado', 'nombrempresa', 'lugarempresa', 'emailempresa',
            'sitiowebempresa', 'nombrecontactoempresarial', 'telefonocontactoempresarial',
            'fechainiciogestion', 'fechafingestion', 'descripcionfunciones',
            'activarparaqueseveaenfront', 'rutacertificado'
        ]
        widgets = {
            'fechainiciogestion': forms.DateInput(attrs={'type': 'date'}),
            'fechafingestion': forms.DateInput(attrs={'type': 'date'}),
            'descripcionfunciones': forms.Textarea(attrs={'rows': 4}),
        }

class ReconocimientosForm(forms.ModelForm):
    class Meta:
        model = Reconocimientos
        fields = [
            'tiporeconocimiento', 'fechareconocimiento', 'descripcionreconocimiento',
            'entidadpatrocinadora', 'nombrecontactoauspicia', 'telefonocontactoauspicia',
            'activarparaqueseveaenfront', 'rutacertificado'
        ]
        widgets = {
            'fechareconocimiento': forms.DateInput(attrs={'type': 'date'}),
            'descripcionreconocimiento': forms.Textarea(attrs={'rows': 3}),
        }

class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        fields = [
            'nombrecurso', 'fechainicio', 'fechafin', 'totalhoras',
            'descripcioncurso', 'entidadpatrocinadora', 'nombrecontactoauspicia',
            'telefonocontactoauspicia', 'emailempresapatrocinadora',
            'activarparaqueseveaenfront', 'rutacertificado'
        ]
        widgets = {
            'fechainicio': forms.DateInput(attrs={'type': 'date'}),
            'fechafin': forms.DateInput(attrs={'type': 'date'}),
            'descripcioncurso': forms.Textarea(attrs={'rows': 3}),
        }

class ProductosAcademicosForm(forms.ModelForm):
    class Meta:
        model = ProductosAcademicos
        fields = ['nombrerecurso', 'clasificador', 'descripcion', 'archivo', 'link', 'activarparaqueseveaenfront']
        widgets = {
            'nombrerecurso': forms.TextInput(attrs={'class': 'form-control'}),
            'clasificador': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://ejemplo.com (Opcional)', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Esto hace que el campo no sea obligatorio en el formulario
        self.fields['link'].required = False

class ProductosLaboralesForm(forms.ModelForm):
    class Meta:
        model = ProductosLaborales
        fields = ['nombreproducto', 'fechaproducto', 'descripcion', 'archivo', 'link', 'activarparaqueseveaenfront']
        widgets = {
            'nombreproducto': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaproducto': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://ejemplo.com (Opcional)', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Esto hace que el campo no sea obligatorio en el formulario
        self.fields['link'].required = False


        
class VentaGarageForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        # Excluimos el perfil (se asigna automático) y la fecha (es auto_now_add)
        exclude = ['idperfilconqueestaactivo', 'fecha_publicacion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estadoproducto': forms.Select(attrs={'class': 'form-control'}),
            'valordelbien': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombreproducto': forms.TextInput(attrs={'class': 'form-control'}),
        }