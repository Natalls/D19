import datetime
from random import randint, seed

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from mmorpg import settings
from sign.forms import RegistrationForm, MyActivationCodeForm
from sign.models import Profile


def generate_code():
    seed()
    return str(randint(10000, 99999))

def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                user_reg = form.save(commit=False)
                user_reg.is_active = False
                form.save()

                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password1')
                u_f = User.objects.get(username=username, email=email, is_active=False)

                author_group = Group.objects.get(name='Author')
                author_group.user_set.add(u_f)

                code = generate_code()

                message = code
                user = authenticate(username=username, password=my_password1)
                now = datetime.datetime.now()

                Profile.objects.create(user=u_f, code=code, date=now)

                send_mail('код подтверждения',
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          [email],
                          fail_silently=False)

                if user and user.is_active:
                    login(request, user)
                    return redirect('/personalArea/')
                else:
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('../activation_code_form')
            else:
                return render(request, 'sign/register.html', {'form': form})
        else:
            return render(request, 'sign/register.html', {'form': RegistrationForm()})
    else:
        return redirect('/personalArea/')

def endreg(request):
    if request.user.is_authenticated:
        return redirect('/personalArea/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if Profile.objects.filter(code=code_use):
                    profile = Profile.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'sign/activation_code_form.html', {'form': form})
                if profile.user.is_active == False:
                    profile.user.is_active = True
                    profile.user.save()
                    print(profile.user.username)
                    print(profile.user.password)
                    user = authenticate(request, username=profile.user.username, password=profile.user.password)
                    print(user)
                    if user is not None:
                        login(request, user)

                    profile.delete()
                    return redirect('/sign/login')
                else:
                    print ('Пользователь уже активирован')
                    form.add_error(None, 'Unknown or disabled account')
                return render(request, 'sign/activation_code_form.html', {'form': form})
            else:
                print('Форма не валидна')
                return render(request, 'sign/activation_code_form.html', {'form': form})
        else:
            print('запрос GET')
            form = MyActivationCodeForm()
            return render(request, 'sign/activation_code_form.html', {'form': form})



