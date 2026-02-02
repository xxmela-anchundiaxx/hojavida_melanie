# curriculum/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Página principal única - Hoja de Vida / Bienvenida
    path('', views.hoja_de_vida, name='hoja_de_vida'),
    
    # Login para admin (usa la URL configurada en settings)
    path('mi_hoja_vida/', auth_views.LoginView.as_view(
        template_name='admin/login.html'
    ), name='login'),
    
    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Generar PDF
    path('pdf/', views.generar_pdf, name='generar_pdf'),
    
    # API para datos
    path('api/datos/', views.api_datos_personales, name='api_datos'),
]