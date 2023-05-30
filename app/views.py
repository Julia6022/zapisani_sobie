from django.db.models import Q, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm, UserProfileForm, LoginForm, MessageForm
from .models import UserProfile, Message, User
from django.urls import reverse_lazy
from datetime import date, timedelta


def index(request):
    return render(request, 'home.html')


################### LOGOWANIE / REJESTRACJA #####################################################

def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app:index')
            else:
                messages.error(request, 'Niepoprawny login lub hasło.')
        else:
            messages.error(request, 'Niepoprawny login lub hasło.')
    else:
        form = LoginForm(request)

    return render(request, 'login.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'Zostałeś wylogowany.')
    return redirect(reverse('app:index'))


def register_request(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password1']
            authenticated_user = authenticate(email=email, password=password)
            login(request, authenticated_user)

            return redirect('app:profile')
        else:
            messages.error(request, 'Niepoprawne dane.')
    else:
        user_form = RegisterForm()

    return render(request, 'register.html', {'user_form': user_form})


################## USER PROFILE #####################################################

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html')


@login_required
def profile_settings(request):
    user = request.user
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('app:profile')
    else:
        profile_form = UserProfileForm(instance=user.userprofile)

    return render(request, 'profile_settings.html', {'profile_form': profile_form})


@login_required
def account_settings(request):
    user = request.user
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            return redirect('app:profile')
    else:
        user_form = RegisterForm(instance=user)

    return render(request, 'account_settings.html', {'user_form': user_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


################## OTHER PROFILES #####################################################

@login_required
def profile_list(request):
    profiles = request.user.userprofile
    name = request.GET.get('name')
    username = request.GET.get('username')
    followed_users = request.GET.get('followed')

    min_age_preference = profiles.min_age_preference
    max_age_preference = profiles.max_age_preference
    sex_preference = profiles.sex_preference

    if sex_preference == 'A':
        if min_age_preference and max_age_preference:
            today = date.today()
            min_birth_date = today - timedelta(days=max_age_preference * 365)
            max_birth_date = today - timedelta(days=min_age_preference * 365)
            filtered_profiles = UserProfile.objects.filter(
                user__date_of_birth__range=(min_birth_date, max_birth_date)
            ).exclude(
                user=request.user
            )
        else:
            filtered_profiles = UserProfile.objects.exclude(
                user=request.user
            )
    else:
        if min_age_preference and max_age_preference:
            today = date.today()
            min_birth_date = today - timedelta(days=max_age_preference * 365)
            max_birth_date = today - timedelta(days=min_age_preference * 365)
            filtered_profiles = UserProfile.objects.filter(
                user__date_of_birth__range=(min_birth_date, max_birth_date),
                user__sex=sex_preference
            ).exclude(
                user=request.user
            )
        else:
            filtered_profiles = UserProfile.objects.filter(
                user__sex=sex_preference
            ).exclude(
                user=request.user
            )

    if name:
        filtered_profiles = filtered_profiles.filter(user__first_name__icontains=name)

    if username:
        filtered_profiles = filtered_profiles.filter(user__username__icontains=username)

    return render(request, 'profile_list.html', {'profiles': filtered_profiles})

@login_required
def user_profile(request, user_id):
    profile = get_object_or_404(User, id=user_id)

    return render(request, 'user_profile.html', {'profile': profile})


############################ WIADOMOŚĆI #####################################################################


@login_required
def inbox(request):
    user = request.user
    sorting_options = request.GET.get('sorting', 'received')
    search_query = request.GET.get('q')

    messages = Message.objects.none()

    if 'received' in sorting_options:
        messages |= Message.objects.filter(receiver=user).order_by('-sent_date')
    if 'sent' in sorting_options:
        messages |= Message.objects.filter(sender=user).order_by('-sent_date')
    if 'read' in sorting_options:
        messages |= Message.objects.filter(receiver=user, is_read=True).order_by('-sent_date')
    if 'unread' in sorting_options:
        messages |= Message.objects.filter(receiver=user, is_read=False).order_by('-sent_date')
    if 'all' in sorting_options:
        messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user).order_by('-sent_date')

    if search_query:
        messages = messages.filter(
            Q(subject__icontains=search_query) |
            Q(body__icontains=search_query) |
            Q(receiver__first_name__icontains=search_query) |
            Q(receiver__username__icontains=search_query)
        )

    context = {
        'messages': messages,
        'sorting_option': sorting_options,
        'search_query': search_query,
    }

    return render(request, 'inbox.html', context)

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'view_message.html', {'message': message})


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('app:inbox')
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form, 'receiver': receiver})


@login_required
def send_reply(request, message_id):
    original_message = Message.objects.get(pk=message_id)

    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        font_size = request.POST['font_size']
        font_family = request.POST['font_family']
        picture = request.POST['picture']
        message = Message.objects.create(sender=request.user, receiver=original_message.sender,
                                         subject=subject, body=body, font_size=font_size, font_family=font_family, picture=picture)
        return redirect('app:inbox')

    return render(request, 'send_reply.html', {'original_message': original_message})