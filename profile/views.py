from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm, LoginForm



def signup(request):
    if request.user.is_authenticated:
        return redirect('product:list')

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')

        try:
            validate_password(password, user)
            user.set_password(password)
            # password field is validated, now save form
            user = form.save()

            # authenticate and login user
            # TODO: send verification code
            # redirect user to verify the code
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            messages.success(request, _('User created successfully!'))
            return redirect('product:list')
        except ValidationError as e:
            form.add_error('password', e)

    context = {
        'form': form
    }
    return render(request, "account/signup.html", context)



def signin(request):
    if request.user.is_authenticated:
        return redirect('product:list')

    form = LoginForm(request.POST or None)

    if form.is_valid():
        phone_number = form.cleaned_data.get('phone_number')
        password = form.cleaned_data.get('password')

        try:
            # authenticate and login user
            user = authenticate(phone_number=phone_number,
                password=password)

            # if credentials were correct, login user
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, _("You're logged in successfully!"))
                return redirect('product:list')
            else:
                messages.error(request, _("Your credentials are incorrect!"))

        except ValidationError as e:
            form.add_error('password', e)

    context = {
        'form': form
    }
    return render(request, "account/login.html", context)



def signout(request):
    if not request.user.is_authenticated:
        return redirect('product:list')

    logout(request)
    messages.info(request, _("You're signed out!"))
    return redirect('product:list')
