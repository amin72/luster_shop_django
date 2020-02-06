from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login

from .forms import SignUpForm



def signup(request):
    form = SignUpForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        phone_number = form.cleaned_data.get('phone_number')
        password = form.cleaned_data.get('password')

        try:
            validate_password(password, user)
            user.set_password(password)
            # password field is validated, now save form
            form.save()

            # authenticate and login user
            new_user = authenticate(phone_number=phone_number,
                password=password)
            login(request, new_user)

            messages.success(request, 'User created successfully!')
            return redirect('product:list')
        except ValidationError as e:
            form.add_error('password', e)

    context = {
        'form': form
    }
    return render(request, "account/signup.html", context)
