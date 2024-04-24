from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .forms import CustomLoginForm, RegisterForm, ForgetPasswordEmailCodeForm, ChangePasswordForm, OtpForm, ProfileEditForm
from .models import OtpCode, CustomUser
from .decorators import only_authenticated_user, redirect_authenticated_user
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

@only_authenticated_user
def home_view(request):
    return render(request, 'users/home.html')

@redirect_authenticated_user
def login_view(request):
    error = None
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username_or_email'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('users:home')
            else:
                error = 'Invalid Credentials'
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form, 'error': error})

@only_authenticated_user
@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')

@redirect_authenticated_user
def registeration_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.source = 'Register'
            user.save()
            # Generar token de activación
            token = default_token_generator.make_token(user)
            # Envía el token a través del método de autenticación predeterminado
            messages.success(request, _('Successfully registered. Please log in to continue.'))  # Mensaje de registro exitoso
            return redirect('users:login')  # Redirigir al usuario al formulario de inicio de sesión
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@redirect_authenticated_user
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgetPasswordEmailCodeForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            user = get_user_model().objects.get(**username_or_email)
            code = get_random_string(20)
            otp = OtpCode(code=code, user=user, email=user.email)
            otp.save()
            try:
                send_reset_password_code(user.email, code)
            except:
                otp.delete()
                messages.error(request, _('Failed while sending code!'))
            else:
                messages.success(request, f"We've sent a password reset otp to your email - {user.email}")
                return redirect('users:reset_code')
    else:
        form = ForgetPasswordEmailCodeForm()
    return render(request, 'users/forgot_password.html', context={'form': form})

@redirect_authenticated_user
def check_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.get(code=form.cleaned_data['otp'])
            user = otp.user
            otp.delete()
            user.is_active = True
            user.save()
            return redirect('users:login')
    else:
        form = OtpForm()
    return render(request, 'users/user_otp.html', {'form': form})

@redirect_authenticated_user
def check_reset_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.get(code=form.cleaned_data['otp'])
            request.session['email'] = otp.user.email
            messages.success(request, "Please create a new password that you don't use on any other site.")
            return redirect('users:reset_new_password')
    else:
        form = OtpForm()
    return render(request, 'users/user_otp.html', {'form': form})

@redirect_authenticated_user
def reset_new_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            email = request.session['email']
            del request.session['email']
            user = CustomUser.objects.get(email=email)
            user.password = make_password(form.cleaned_data["new_password2"])
            user.save()
            messages.success(request, "Your password changed. Now you can login with your new password.")
            return redirect('users:login')
    else:
        form = ChangePasswordForm()
    return render(request, 'users/new_password.html', {'form': form})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            # Guardar los cambios en el perfil del usuario
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        # Crear el formulario pre-populado con los datos del usuario
        form = ProfileEditForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})
@login_required
def get_user_data(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'cedula': user.cedula,  # Agrega otros campos que quieras devolver
        'telefono': user.telefono,
        'direccion': user.direccion
    }
    return JsonResponse(data)