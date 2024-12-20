from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from perfil.forms import PerfilForm
from contas.permissions import grupo_colaborador_required
from contas.models import MyUser
from contas.forms import CustomUserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def timeout_view(request):
    return render(request, 'timeout.html')


def timeout_view(request):
    return render(request, 'timeout.html')


def logout_view(request):
    logout(request)
    return redirect('home')

# Mudança de Senha Force (first_login)


@login_required
def force_password_change_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.force_change_password = False  # passa o parametro para False.
            user.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'registration/password_force_change_form.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

# register


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, user=request.user)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_valid = False
            usuario.save()

            group = Group.objects.get(name='usuario')
            usuario.groups.add(group)

            messages.success(
                request, 'Registrado. Agora faça o login para começar!')
            return redirect('login')
        else:
            # Tratar quando usuario já existe, senhas... etc...
            messages.error(request, 'A senha deve ter pelo menos 1 caractere maiúsculo, \
                1 caractere especial e no minimo 8 caracteres.')
    form = CustomUserCreationForm(user=request.user)
    return render(request, "register.html", {"form": form})

# TODO atualizar USUARIO


@login_required()
def atualizar_meu_usuario(request):
    if request.method == 'POST':
        form = UserChangeForm(
            request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user, user=request.user)
    return render(request, 'user_update.html', {'form': form})

# Atualizar qualquer usuário pelo parametro usermane


@login_required()
@grupo_colaborador_required(['administrador', 'colaborador'])
def atualizar_usuario(request, usermane):
    user = get_object_or_404(MyUser, username=usermane)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(request.POST, instance=user, user=request.user)
    return render(request, 'user_update.html', {'form': form})

# TODO Validando se o usuário é colaborador e colaborador


@login_required
@grupo_colaborador_required(['administrador', 'colaborador'])
def lista_usuarios(request):  # Lista Cliente
    lista_usuarios = MyUser.objects.select_related(
        'perfil').filter(is_superuser=False)
    return render(request, 'lista-usuarios.html', {'lista_usuarios': lista_usuarios})


@login_required
@grupo_colaborador_required(['administrador', 'colaborador'])
def adicionar_usuario(request):
    user_form = CustomUserCreationForm(request.POST, user=request.user)
    perfil_form = PerfilForm(request.POST, request.FILES, user=request.user)

    if user_form.is_valid() and perfil_form.is_valid():
        # Salve o usuário
        usuario = user_form.save()

        # Crie um novo perfil para o usuário
        perfil = perfil_form.save(commit=False)
        perfil.usuario = usuario
        perfil.save()

        messages.success(request, 'Usuário adicionado com sucesso.')
        return redirect('lista_usuarios')
    else:
        #Verifica os erros individualmente para cada campo de formulário
        for field, error_list in user_form.errors.items():
            for error in error_list:
                messages.error(request, f"Erro no campo '{user_form.fields[field].label}': {error}")
            for field, error_list in perfil_form.errors.items():
                for error in error_list:
                    messages.error(request, f"Erro no campo '{perfil_form.fields[field].label}': {error}")    
                    
        context = {'user_form': user_form, 'perfil_form': perfil_form}
        return render(request, "adicionar-usuario.html", context)
        
        
        
        
        # # erros
        # # if not user_form.cleaned_data.get("email"):
        # #     user_form.add_error("email", "Email obrigatório.")
        # # if MyUser.objects.filter(email=user_form.cleaned_data.get("email")).exists():
        # #     user_form.add_error("email", "Email em uso.")

        # error_list1 = user_form.errors.as_text()
        # error_list2 = perfil_form.errors.as_text()
        # # Você pode fazer o que quiser com erros
        # messages.error(request, error_list1)
        # messages.error(request, error_list2)

        # return render(request, "adicionar-usuario.html", {'user_form': user_form, 'perfil_form': perfil_form})

    
