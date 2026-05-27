from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path, include
from inscricoes.views import listar_inscricoes

urlpatterns = [

    path('admin/', admin.site.urls),

    path(
        '',
        listar_inscricoes,
        name='home'
    ),

    path(
        'api/inscricoes/',
        include('inscricoes.urls')
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    


]