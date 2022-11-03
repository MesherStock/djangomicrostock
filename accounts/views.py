from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import User
from django.contrib import auth, messages
from django.contrib.auth import logout, login, authenticate

#User Account Verification
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage





# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            msg = EmailMessage(mail_subject, message, to=[to_email])
            msg.send()

            # messages.success(request, "Thank you for registering with us. ")
            
            return redirect("/account/login/?command=verification&email="+email)

    else:
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/register.html', context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('/')
        
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'accounts/login.html')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated ")
        return redirect("account:login")

    else:
        messages.error(request, "Invalid activation")
        return redirect("account:register")


def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect('/')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Please Reset Your Password"
            message = render_to_string('accounts/forgot_activate_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            msg = EmailMessage(mail_subject, message, to=[to_email])
            msg.send()
            messages.success(request, 'Password reset email had been sent to your email address')
            return redirect('account:login')
        
        else:
            messages.error(request, "Account doesn't exist")
            return redirect('account:forgotPassword')
    return render(request, "accounts/forgotPassword.html")



def password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid 
        messages.success(request, 'Please reset your password')
        return redirect('account:resetPassword')
    
    else:
        messages.error(request, 'This link has been expired')
        return redirect("account:login")
    

def reset_Password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('account:login')
        
        else:
            messages.error(request, 'Password do not match')
            return redirect('account:resetPassword')
    
    else:
        return render(request, 'accounts/reset_Password.html')

