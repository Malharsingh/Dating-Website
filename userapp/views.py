from datetime import date

from cities_light.models import City
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from datingapp.models import Favorite
from .forms import UserUpdateForm, ProfileUpdateForm, SignUpStepOneForm, SignUpStepTwoForm, SignUpStepThreeForm, \
    PasswordResetForm
from .models import Profile


def update_visit_count(request):
    # Check if 'num_visits' key exists in session for the current date
    today = date.today().isoformat()
    if 'num_visits' in request.session and request.session['date_visited'] == today:
        request.session['num_visits'] += 1
    else:
        request.session['num_visits'] = 1
        request.session['date_visited'] = today


def home(request):
    """Home page"""
    update_visit_count(request)
    if request.user.is_authenticated:
        return redirect('datingapp:dating')
    return render(request, template_name='userapp/landing_page.html')


def signup(request):
    """User registration"""
    if request.user.is_authenticated:  # If the user is logged in, then he does not have access to the login form
        update_visit_count(request)
        return redirect('datingapp:dating')
    else:
        update_visit_count(request)
        error_context = []
        if request.method == 'GET':
            return render(request, template_name='userapp/sign_up.html', context={'form': UserCreationForm})
        else:
            if not (request.POST['username']):
                error_context.append('Login can\'t be empty')
            elif not (request.POST['password1']):
                error_context.append('Password can\'t be empty')
            elif not (request.POST['password2']):
                error_context.append('Confirm Password can\'t be empty')
            elif request.POST['password1'] != request.POST['password2']:
                error_context.append('Password did not match')
            elif len(request.POST['password1']) < 8:
                error_context.append('Password less then 8 characters')
            elif str(request.POST['username']).lower() in ['admin', 'аdmin', 'god', 'administrator',
                                                           'аdministrator', 'аdministrаtor']:
                error_context.append('This login can\'t be taken')
            else:
                try:
                    user = User.objects.create_user(username=request.POST['username'],
                                                    password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('userapp:sign_up_step_one')
                except IntegrityError:
                    error_context.append('That username has already been taken')
                    return render(request, template_name='userapp/sign_up.html',
                                  context={'form': UserCreationForm(), 'error_context': error_context})
            return render(request, template_name='userapp/sign_up.html',
                          context={'form': UserCreationForm(), 'error_context': error_context})


def signin(request):
    """User Login"""
    if request.user.is_authenticated:  # If the user is logged in, then he does not have access to the login form
        update_visit_count(request)
        return redirect('datingapp:dating')
    else:
        update_visit_count(request)
        if request.method == 'GET':
            return render(request, template_name='userapp/sign_in.html',
                          context={'form': AuthenticationForm()})
        else:
            user = authenticate(request, username=request.POST['username'],
                                password=request.POST['password'])
            if user is None:
                return render(request, template_name='userapp/sign_in.html',
                              context={'form': AuthenticationForm(),
                                       'error_signin': 'Username or password did not match'})
            else:
                login(request, user)
                return redirect('datingapp:dating')


@login_required
def logout_user(request):
    """User logout"""
    if request.method == 'POST':
        logout(request)
        response = redirect('home')
        response.delete_cookie('favorites_count')
        response.delete_cookie('favorites')
        return response


@login_required
def user_account(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.about:
        """Personal userapp account where he can edit userapp data"""
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

            city = request.POST.get('city')
            city_name = city.split(',')[0].strip() if ',' in city else city.split(' ')[0].strip()

            errors = []

            if int(request.POST.get('age', 0)) < 18:
                errors.append('Your age must be at least 18 years old')
            elif not str(request.POST.get('age', '')).isnumeric():
                errors.append('Incorrect age field')

            if len(request.POST.get('about', '')) < 50:
                errors.append('About field must be at least 50 characters')

            if not City.objects.filter(name_ascii__iexact=city_name).exists():
                errors.append('Choose a correct city')

            if errors:
                # Pass errors list to the template
                return render(request, template_name='userapp/user_account.html',
                              context={'errors': errors, 'u_form': u_form, 'p_form': p_form})

            try:
                u_form.save()
                p_form.save()
                return redirect('userapp:user_account')  # Redirect to user profile page
            except ValueError:
                errors.append('Files are too large, requirement is less than 2.5 MB')
                return render(request, template_name='userapp/user_account.html',
                              context={'errors': errors, 'u_form': u_form, 'p_form': p_form})
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        favorites = Favorite.objects.filter(user=request.user)
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'favorites': favorites.order_by('-saved_date'),
            'favorites_count': favorites.count(),
        }

        return render(request, template_name='userapp/user_account.html', context=context)

    return redirect('userapp:sign_up_step_three')


@login_required
def sign_up_step_one(request):
    if request.method == 'POST':
        step_one_form = SignUpStepOneForm(request.POST, request.FILES, instance=request.user.profile)

        errors = []

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        age = request.POST.get('age', '').strip()

        if not first_name:
            errors.append('First name can\'t be empty')
        elif not first_name.isalpha():
            errors.append('First name can\'t have numbers')

        if first_name.lower() == request.user.username.lower():
            errors.append('First name can\'t be the same as username')

        if not last_name:
            errors.append('Last name can\'t be empty')
        elif not last_name.isalpha():
            errors.append('Last name can\'t have numbers')

        if not age:
            errors.append('Age can\'t be empty')
        elif not age.isnumeric():
            errors.append('Incorrect age field')
        elif int(age) < 18:
            errors.append('Your age must be at least 18 years old')

        if errors:
            # Pass errors list to the template
            return render(request, template_name='userapp/sign_up_step_one.html',
                          context={'errors': errors, 'step_one_form': step_one_form})

        step_one_form.save()
        return redirect('userapp:sign_up_step_two')
    else:
        step_one_form = SignUpStepOneForm(instance=request.user.profile)

    context = {
        'step_one_form': step_one_form,
    }
    return render(request, template_name='userapp/sign_up_step_one.html', context=context)


@login_required
def sign_up_step_two(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.first_name and profile.last_name and profile.age:
        if request.method == 'POST':
            step_two_form = SignUpStepTwoForm(request.POST, request.FILES, instance=request.user.profile)

            errors = []

            city = request.POST.get('city', '').strip()
            city_name = city.split(', ')[0].strip() if ', ' in city else city.split(' ')[0].strip()

            if not city:
                errors.append('Location can\'t be empty')
            elif not City.objects.filter(name_ascii__iexact=city_name).exists():
                errors.append('Choose a correct city')

            if request.POST.get('sex', '') not in ['M', 'F']:
                errors.append('Choose correct sex field')

            if request.POST.get('seeking', '') not in ['M', 'F']:
                errors.append('Choose correct seeking field')

            if errors:
                # Pass errors list to the template
                return render(request, template_name='userapp/sign_up_step_two.html',
                              context={'errors': errors, 'step_two_form': step_two_form})

            step_two_form.save()
            return redirect('userapp:sign_up_step_three')
        else:
            step_two_form = SignUpStepTwoForm(instance=request.user.profile)

        context = {
            'step_two_form': step_two_form,
        }
        return render(request, template_name='userapp/sign_up_step_two.html', context=context)
    return redirect('userapp:sign_up_step_one')


@login_required
def sign_up_step_three(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.city and profile.sex and profile.seeking:
        if request.method == 'POST':
            step_three_form = SignUpStepThreeForm(request.POST, request.FILES, instance=request.user.profile)

            errors = []

            if len(request.POST.get('about', '').strip()) < 50:
                errors.append('About field must be at least 50 characters')

            if errors:
                # Pass errors list to the template
                return render(request, template_name='userapp/sign_up_step_three.html', context={'errors': errors, 'step_three_form': step_three_form})

            try:
                step_three_form.save()
                return redirect('datingapp:dating')
            except ValueError:
                errors.append('File is too large, requirement is less than 2.5 MB')
                return render(request, template_name='userapp/sign_up_step_three.html', context={'errors': errors, 'step_three_form': step_three_form})

        else:
            step_three_form = SignUpStepThreeForm(instance=request.user.profile)

        context = {
            'step_three_form': step_three_form,
        }
        return render(request, template_name='userapp/sign_up_step_three.html', context=context)
    return redirect('userapp:sign_up_step_two')


def forget_password_action(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            return redirect(to='userapp:password_reset_form', user_id=user.id)
        else:
            messages.error(request, message='Username does not exist')
            return redirect('userapp:forget_password_action')

    return render(request, template_name='userapp/forget_password.html')


def password_reset_form(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, message='Your password has been successfully reset.')
                return redirect('userapp:signin')  # Adjust as needed
            else:
                messages.error(request, message='The passwords do not match.')
    else:
        form = PasswordResetForm()

    return render(request, template_name='userapp/password_reset_form.html', context={'form': form})
