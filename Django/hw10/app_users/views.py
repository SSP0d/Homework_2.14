from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'app_users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='quote_site:index')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your account was successfully created!')
            return redirect(to='users:login')

        return render(request, self.template_name, {'form': self.form_class()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('app_users:logout')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='app_users:login')

        login(request, user)
        return redirect(to='app_quotes:index')

    return render(request, 'app_users/login.html', context={'form': LoginForm()})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'app_users/password_reset.html'
    email_template_name = 'app_users/password_reset_email.html'
    html_email_template_name = 'app_users/password_reset_email.html'
    success_url = reverse_lazy('app_users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'app_users/password_reset_subject.txt'
