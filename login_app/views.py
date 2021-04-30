from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import django_rq
from . models import PasswordResetRequest, RequestEmail
from . messaging import email_message


def sign_up(request):
    context = {}
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_name = request.POST['user']
        email = request.POST['email']
        if password == confirm_password:
            if User.objects.create_user(user_name, email, password):
                return HttpResponseRedirect(reverse('login_app:request_token'))
            else:
                context = {
                    'error': 'Could not create user account - please try again.'
                }
        else:
            context = {
                'error': 'Passwords did not match. Please try again.'
            }
    return render(request, 'login_app/sign_up.html', context)


def request_token(request):
    if request.method == "POST" and 'sendButton' in request.POST:
        post_user_email = request.POST['email']
        user = None

        if post_user_email:
            try:
                user = User.objects.get(email=post_user_email)
            except:
                print(f"Invalid request: {post_user_email}")
        else:
            print(f"Invalid email: {post_user_email}")
        if user:
            request_email = RequestEmail()
            request_email.user = user
            request_email.save()
            django_rq.enqueue(email_message, {
                'token': request_email.token,
                'email': request_email.user.email,
            })
            messages.success(request, 'We sent you a token on your email')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if request.method == "POST" and 'submitButton' in request.POST:
        token = request.POST['token']
        if token:
            try:
                email_request = RequestEmail.object.get(token=token)
                email_request.save()
            except:
                print("Invalid attempt.")

            return HttpResponseRedirect(reverse('login_app:login'))

    return render(request, 'login_app/request_token.html')


def login(request):
    context = {}

    if request.method == "POST":
        user = authenticate(
            request, username=request.POST['user'], password=request.POST['password'])
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('bank_app:index'))
        else:
            context = {
                'error': 'Bad username or password.',
            }
    return render(request, 'login_app/login.html')


def logout(request):
    dj_logout(request)
    return render(request, 'login_app/login.html')


def delete_account(request):
    pass


def password_reset_request(request):
    if request.method == "POST":
        post_user = request.POST['user']
        user = None

        if post_user:
            try:
                user = User.objects.get(username=post_user)
            except:
                print(f"Invalid password request: {post_user}")
    else:
        post_user = request.POST['email']
        try:
            user = User.objects.get(email=post_user)
        except:
            print(f"Invalid password request: {post_user}")
    if user:
        prr = PasswordResetRequest()
        prr.user = user
        prr.save()
        print(prr)
        return HttpResponseRedirect(reverse('login_app:password_reset'))
    return render(request, 'login_app/password_reset_request.html')


def password_reset(request):
    if request.method == "POST":
        post_user = request.POST['user']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        token = request.POST['token']

        if password == confirm_password:
            try:
                prr = PasswordResetRequest.objects.get(token=token)
                prr.save()
            except:
                print("Invalid reset attempt.")
                return render(request, 'login_app/password_reset.html')
            user = prr.user
            user.set_password(password)
            return HttpResponseRedirect(reverse('login_app:login'))
    return render(request, 'login_app/password_reset.html')
