from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .forms import *
from .models import *

def inicioView(request):
	return render(request, "inicio.html", {})

def iniciarSesionView(request):
	formulario = iniciarSesionForm(request.POST or None)
	contexto = {"formulario": formulario}

	if formulario.is_valid():
		datos_formulario = formulario.cleaned_data
		nombre_obtenido = datos_formulario.get("nombre")
		contrasena_obtenida = datos_formulario.get("contrasena")

		objeto_usuario = Usuario.objects.get(nombre = nombre_obtenido)

		if contrasena_obtenida == objeto_usuario.contrasena:
			return HttpResponseRedirect(reverse('inicio'))

	return render(request, "iniciar_sesion.html", contexto)

def mostrarProductoView(request):
	productos = Producto.objects.all()
	contexto = {"productos": productos}

	return render(request, "productos.html", contexto)

def registrarProductoView(request):
	formulario = registrarProductoForm(request.POST or None)
	contexto = {"formulario": formulario}

	if formulario.is_valid():
		datos_formulario = formulario.cleaned_data
		nombre_obtenido = datos_formulario.get("nombre")
		tipo_obtenido = datos_formulario.get("tipo")
		valor_obtenido = datos_formulario.get("valor")

		objeto_proveedor = Producto.objects.create(nombre = nombre_obtenido,
                                                   tipo = tipo_obtenido,
                                                   valor = valor_obtenido)

		return HttpResponseRedirect(reverse('inicio'))

	return render(request, "registrar_producto.html", contexto)

def proveedorView(request):
	proveedores = Proveedor.objects.all()
	contexto = {"proveedores": proveedores}

	return render(request, "proveedores.html", contexto)

def registrarProveedorView(request):
	formulario = registrarProveedorForm(request.POST or None)
	contexto = {"formulario": formulario}

	if formulario.is_valid():
		datos_formulario = formulario.cleaned_data
		nombre_obtenido = datos_formulario.get("nombre")
		telefono_obtenido = datos_formulario.get("telefono")
		direccion_obtenida = datos_formulario.get("direccion")
		correo_obtenido = datos_formulario.get("correo")

		objeto_proveedor = Proveedor.objects.create(nombre = nombre_obtenido,
                                                    telefono = telefono_obtenido,
                                                    direccion = direccion_obtenida,
                                                    correo = correo_obtenido)

		return HttpResponseRedirect(reverse('inicio'))

	return render(request, "registrar_proveedor.html", contexto)

def almacenView(request):
	almacenes = Almacen.objects.all()
	contexto = {"almacenes": almacenes}

	return render(request, "almacenes.html", contexto)

def pedidoView(request):
	formulario_tipo_pedido = seleccionarTipoPedidoForm(request.POST or None)

	if formulario_tipo_pedido.is_valid():
		datos_formulario = formulario_tipo_pedido.cleaned_data
		tipo_pedido_obtenido = datos_formulario.get("tipo_pedido")

		if tipo_pedido_obtenido == 'todos_los_pedidos':
			pedidos = Pedido.objects.all()
		if tipo_pedido_obtenido == 'pedidos_recibidos':
			pedidos = Pedido.objects.filter(fecha_recibida__isnull = False)
		if tipo_pedido_obtenido == 'pedidos_no_recibidos':
			pedidos = Pedido.objects.filter(fecha_recibida__isnull = True)
	else:
		pedidos = Pedido.objects.all()

	contexto = {"formulario_tipo_pedido": formulario_tipo_pedido, "pedidos": pedidos}

	return render(request, "pedidos.html", contexto)

def registrarPedidoView(request):
	formulario = registrarPedidoForm(request.POST or None)
	contexto = {"formulario": formulario}

	if formulario.is_valid():
		datos_formulario = formulario.cleaned_data
		producto_obtenido = datos_formulario.get("producto")
		proveedor_obtenido = datos_formulario.get("proveedor")
		cantidad_obtenida = datos_formulario.get("cantidad")

		producto = Producto.objects.get(nombre = producto_obtenido)
		proveedor = Proveedor.objects.get(nombre = proveedor_obtenido)
		administrador = Usuario.objects.get(nombre = 'administrador')

		correo_emisor = administrador.correo
		correo_emisor_contrasena = administrador.contrasena

		correo_receptor = proveedor.correo

		mensaje = MIMEMultipart('mixed')
		mensaje['From'] = correo_emisor
		mensaje['To'] = correo_receptor
		mensaje['Subject'] = '[Pedido] - ' + producto.nombre

		mensaje_texto = MIMEText('Cantidad: ' + str(cantidad_obtenida), 'plain')
		mensaje.attach(mensaje_texto)

		try:
			servidor = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			servidor.ehlo()
			servidor.login(correo_emisor, correo_emisor_contrasena)
			servidor.sendmail(correo_emisor, correo_receptor, mensaje.as_string())
			servidor.close()

			print('Exito. Se ha enviado el correo')
		except:
			print('Error. No se ha podido enviar el correo')

		return HttpResponseRedirect(reverse('inicio'))

	return render(request, "registrar_pedido.html", contexto)

def registrarUsuarioView(request):
	formulario = registrarUsuarioForm(request.POST or None)
	contexto = {"formulario": formulario}

	if formulario.is_valid():
		datos_formulario = formulario.cleaned_data
		nombre_obtenido = datos_formulario.get("nombre")
		contrasena_obtenida = datos_formulario.get("contrasena")
		correo_obtenido = datos_formulario.get("email")

		objeto_usuario = Usuario.objects.create(nombre = nombre_obtenido,
                                                contrasena = contrasena_obtenida,
                                                correo = correo_obtenido)

	return render(request, "registrar_usuario.html", contexto)

def reporteProductoView(request):
	from django.db import connection
	cursor = connection.cursor()

	formulario = reporteProductoForm(request.POST)

	if formulario.is_valid():
		datos_formulario = formulario.cleaned_data
		mes = datos_formulario.get('DateField', 'month')

	cursor.execute("SELECT aplicacion_producto.nombre, cantidad, fecha_recibida, aplicacion_proveedor.nombre FROM aplicacion_pedido INNER JOIN aplicacion_producto ON aplicacion_pedido.producto_id = aplicacion_producto.id INNER JOIN aplicacion_proveedor ON aplicacion_pedido.proveedor_id = aplicacion_proveedor.id;")
	productos = cursor.fetchall()

	contexto = {"formulario": formulario, "productos": productos}

	return render(request, "reporte_productos.html", contexto)

def proveedorProductoView(request, id_propro):
	productos = Producto.objects.filter(proveedorproducto__producto__id__isnull = False,
                                        proveedorproducto__proveedor__id = id_propro)

	contexto = {"productos": productos}

	return render(request, "proveedor_producto.html", contexto)