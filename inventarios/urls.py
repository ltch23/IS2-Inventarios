"""inventarios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from aplicacion import views

urlpatterns = [url(r'^admin/',
                   admin.site.urls),

               url(r'^$',
                   views.iniciarSesionView,
                   name = 'iniciar_sesion'),

               url(r'^inicio/',
                   views.inicioView,
                   name = 'inicio'),

               url(r'^productos/',
                   views.mostrarProductoView,
                   name = 'productos'),

               url(r'^registrar_producto/',
                   views.registrarProductoView,
                   name = 'registrar_producto'),

               url(r'^registrar_proveedor/',
                   views.registrarProveedorView,
                   name = 'registrar_proveedor'),

               url(r'^proveedores/',
                   views.proveedorView,
                   name = 'proveedores'),

               url(r'^almacenes/',
                   views.almacenView,
                   name = 'almacenes'),

               url(r'^pedidos/',
                   views.pedidoView,
                   name = 'pedidos'),

               url(r'^registrar_usuario/',
                   views.registrarUsuarioView,
                   name = 'registrar_usuario'),

               url(r'^registrar_pedido/',
                   views.registrarPedidoView,
                   name = 'registrar_pedido'),

               url(r'^proveedor_producto/(?P<id_propro>\d+)/$',
                   views.proveedorProductoView,
                   name = 'proveedor_producto'),

               url(r'^reporte_productos/',
                   views.reporteProductoView,
                   name = 'reporte_productos')]