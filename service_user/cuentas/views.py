import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import Usuario

@csrf_exempt
def registro_usuario(request):
    if request.method == 'POST':
        data = request.POST
        campos_obligatorios = ['cedula', 'nombre', 'direccion', 'telefono', 'password', 'correo']
        for campo in campos_obligatorios:
            if campo not in data:
                return JsonResponse({'error': f'Campo {campo} es obligatorio'}, status=400)
        cedula = data.get('cedula')
        if not validar_formato_cedula(cedula):
            return JsonResponse({'error': 'Formato de cédula incorrecto'}, status=400)
        nombre = data.get('nombre')
        if not validar_formato_nombre(nombre):
            return JsonResponse({'error': 'Formato de nombre incorrecto'}, status=400)
        telefono = data.get('telefono')
        if not validar_formato_telefono(telefono):
            return JsonResponse({'error': 'Formato de teléfono incorrecto'}, status=400)
        correo = data.get('correo')
        if not validar_formato_correo(correo):
            return JsonResponse({'error': 'Formato de correo electrónico incorrecto'}, status=400)
        if Usuario.objects.filter(correo=correo).exists():
            return JsonResponse({'error': 'El correo electrónico ya está en uso'}, status=400)
        nuevo_usuario = Usuario(
            cedula=cedula,
            nombre=nombre,
            direccion=data.get('direccion'),
            telefono=telefono,
            password=data.get('password'),
            correo=correo
        )
        nuevo_usuario.save()
        return JsonResponse({'mensaje': 'Usuario registrado correctamente'}, status=201)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def validar_formato_cedula(cedula):
    return re.match(r'^[0-9]{9}$', cedula)

def validar_formato_nombre(nombre):
    return bool(re.match(r'^[a-zA-Z\s]+$', nombre))

def validar_formato_telefono(telefono):
    return re.match(r'^[0-9]{10}$', telefono)

def validar_formato_correo(correo):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+$', correo))

@csrf_exempt
def actualizar_usuario(request, id_usuario):
    if request.method == 'PUT':
        usuario = Usuario.objects.get(id=id_usuario)
        data = request.POST
        campos_validos = ['cedula', 'nombre', 'direccion', 'telefono', 'password']
        errores = {}
        for campo in campos_validos:
            valor = data.get(campo)
            if valor:
                if campo == 'cedula':
                    if not validar_formato_cedula(valor):
                        errores[campo] = 'Formato de cédula incorrecto'
                elif campo == 'nombre':
                    if not validar_formato_nombre(valor):
                        errores[campo] = 'Formato de nombre incorrecto'
                elif campo == 'direccion':
                    if not validar_formato_direccion(valor):
                        errores[campo] = 'Formato de dirección incorrecto'
                elif campo == 'telefono':
                    if not validar_formato_telefono(valor):
                        errores[campo] = 'Formato de teléfono incorrecto'
                elif campo == 'password':
                    if not validar_formato_password(valor):
                        errores[campo] = 'Formato de contraseña incorrecto'
                setattr(usuario, campo, valor)
        if errores:
            return JsonResponse({'errores': errores}, status=400)
        else:
            usuario.save()
            return JsonResponse({'mensaje': 'Usuario actualizado correctamente'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def validar_formato_direccion(direccion):
    if not direccion:
        return False
    if len(direccion) > 100:
        return False
    return bool(re.match(r'^[a-zA-Z0-9\s.,#\-]+$', direccion))

@csrf_exempt
def obtener_usuario(request, id_usuario):
    if request.method == 'GET':
        usuario = Usuario.objects.get(id=id_usuario)
        datos_usuario = {
            'cedula': usuario.cedula,
            'nombre': usuario.nombre,
            'direccion': usuario.direccion,
            'telefono': usuario.telefono,
            'correo': usuario.correo,
        }
        return JsonResponse(datos_usuario, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        correo = request.POST.get('correo', '')  
        password = request.POST.get('password', '')
        
        print("Correo recibido:", correo)
        print("Contraseña recibida:", password)

        if any(re.findall(r'[;\'"]', correo + password)):
            return JsonResponse({'error': 'Campos no válidos'}, status=400)

        user = authenticate(request, correo=correo, password=password)
        
        print("Usuario autenticado:", user)

        if user is not None:
            login(request, user)
            return JsonResponse({'token': user.auth_token.key})
        else:
            return JsonResponse({'error': 'Credenciales incorsaarectas'}, status=401)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def cerrar_sesion(request):
    logout(request)
    return JsonResponse({'mensaje': 'Sesión cerrada correctamente'})