from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import arrow
from .forms import *
from .models import *

def InicioView(request):
	return render(request, "inicio.html", {})

def IniciarSesionView(request):
        formulario = IniciarSesionForm(request.POST or None)
        contexto = { "formulario" : formulario }

        if formulario.is_valid():
                print(formulario.cleaned_data)
                datos_formulario = formulario.cleaned_data
                nombre_obtenido = datos_formulario.get("nombre_form")
                contrasena_obtenida = datos_formulario.get("contrasena_form")

                objeto_usuario = Usuario.objects.get(nombre = nombre_obtenido)
                datos_formulario = formulario.cleaned_data
                nombre_obtenido = datos_formulario.get("nombre_form")
                contrasena_obtenida = datos_formulario.get("contrasena_form")
                objeto_usuario = Usuario.objects.get(nombre = nombre_obtenido)

                if contrasena_obtenida == objeto_usuario.contrasena:
                        return HttpResponseRedirect(reverse('inicio'))

        return render(request, "iniciar_sesion.html", contexto)


def mostrarProductoView(request):
        productos = Producto.objects.all()
        contexto = { "productos" : productos }
        return render(request,"mostrarProducto.html",contexto)

def registrarProductoView(request):
        formulario = RegistrarProductoForm(request.POST or None)
        contexto = { "formulario" : formulario }
        if formulario.is_valid():
                print(formulario.cleaned_data)
                datos_formulario = formulario.cleaned_data
                nombre_obtenido = datos_formulario.get("nombre_form")
                tipo_obtenido = datos_formulario.get("tipo_form")
                valor_obtenido = datos_formulario.get("valor_form")
                objeto_proveedor = Producto.objects.create(nombre = nombre_obtenido, tipo = tipo_obtenido, valor = valor_obtenido)
                return HttpResponseRedirect(reverse('inicio'))	
        return render(request, "registrarProducto.html", contexto)
def ProveedorView(request):
	proveedores = Proveedor.objects.all()
	contexto = { "proveedores" : proveedores }
	
	return render(request, "proveedor.html", contexto)

def RegistrarProveedorView(request):
	formulario = RegistrarProveedorForm(request.POST or None)
	contexto = { "formulario" : formulario }

	if formulario.is_valid():
		print(formulario.cleaned_data)

		datos_formulario = formulario.cleaned_data
		nombre_obtenido = datos_formulario.get("nombre_form")
		telefono_obtenido = datos_formulario.get("telefono_form")
		direccion_obtenida = datos_formulario.get("direccion_form")
		email_obtenido = datos_formulario.get("email_form")

		objeto_proveedor = Proveedor.objects.create(nombre = nombre_obtenido, telefono = telefono_obtenido, direccion = direccion_obtenida, email = email_obtenido)

		return HttpResponseRedirect(reverse('inicio'))
		
	return render(request, "registrar_proveedor.html", contexto)

def AlmacenView(request):
    almacenes = Almacen.objects.all()
    contexto = { "almacenes" : almacenes }

    return render(request, "almacen.html", contexto)

def PedidoView(request):
	pedidos = Pedido.objects.all()
	contexto = { 'pedidos' : pedidos }

	return render(request, 'pedido.html', contexto)

def RegistrarUsuarioView(request):
    formulario = RegistrarUsuarioForm(request.POST or None)
    contexto = { "formulario" : formulario }

    if formulario.is_valid():
        print(formulario.cleaned_data)

        datos_formulario = formulario.cleaned_data
        nombre_obtenido = datos_formulario.get("nombre_form")
        contrasena_obtenido=datos_formulario.get("contrasena_form")
        email_obtenido = datos_formulario.get("email_form")

        objeto_usuario = Usuario.objects.create(nombre = nombre_obtenido, contrasena=contrasena_obtenido, email = email_obtenido)

        return HttpResponseRedirect(reverse('inicio'))
        
    return render(request, "usuario_form.html", contexto)


class AnalyticsIndexView(TemplateView):
    template_name = 'analytics/admin/index.html'

    def get_context_data(self, **kwargs):
        context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context['30_day_registrations'] = self.thirty_day_registrations()
        return context

    def thirty_day_registrations(self):
        final_data = []

        date = arrow.now()
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = User.objects.filter(
                date_joined__gte=date.floor('day').datetime,
                date_joined__lte=date.ceil('day').datetime).count()
            final_data.append(count)

        return final_data
