from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
# TODO Obrigando o usuario estar logado p acessar a view (atualizar_usuario) Função login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from contas.models import MyUser
from contas.forms import CustomUserCreationForm, UserChangeForm
from django.contrib import messages


def timeout_view(request):
    return render(request, 'timeout.html')

# TODO add urls.py um path para logout


def logout_view(request):
    logout(request)
    return redirect('home')


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
        form = CustomUserCreationForm(request.POST)
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
    form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required()
def atualizar_meu_usuario(request):
    if request.method == 'POST': #TODO pegar os dados/user preenchidos
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'user_update.html', {'form': form})


@login_required()
def atualizar_usuario(request, user_id): # TODO usar a mesma rota com (user_id).
    user = get_object_or_404(MyUser, pk=user_id)
    if request.method == 'POST':
        # TODO A instancia é meu user autenticado
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'O perfil de usuário foi atualizado com sucesso!')
            return redirect('home')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'user_update.html', {'form': form}) # TODO usar o mesmo template
