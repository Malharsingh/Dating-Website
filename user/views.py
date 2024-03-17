from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from forms import SignUpStepOneForm, UserUpdateForm, ProfileUpdateForm
from user.models import Profile


# Create your views here.
def signup_one(request):
    if request.method == 'POST':
        step_one_form = SignUpStepOneForm(request.POST, request.FILES, instance=request.user.profile)

        if not (request.POST['first_name']):
            return render(request, 'user/signup_step_one.html', {'error': 'First name can\'t be empty'})
        if not (str(request.POST['first_name']).isalpha()):
            return render(request, 'user/signup_step_one.html', {'error': 'First name can\'t have numbers'})
        elif not (request.POST['last_name']):
            return render(request, 'user/signup_step_one.html', {'error': 'Last name can\'t be empty'})
        if not (str(request.POST['last_name']).isalpha()):
            return render(request, 'user/signup_step_one.html', {'error': 'Last name can\'t have numbers'})
        elif not (request.POST['age']):
            return render(request, 'user/signup_step_one.html', {'error': 'Age can\'t be empty'})
        elif int(request.POST['age']) < 18:
            return render(request, 'user/signup_step_one.html', {'error': 'Your age must be at least 18 years old'})
        elif not str(request.POST['age']).isnumeric():
            return render(request, 'user/signup_step_one.html', {'error': 'Uncorrect age field'})
        else:
            step_one_form.save()
            return redirect('user_app:signup_two')
    else:
        step_one_form = SignUpStepOneForm(instance=request.user.profile)

    context = {
        'step_one_form': step_one_form,
    }
    return render(request, 'user/signup_step_one.html', context)


@login_required
def user_account(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.about:
        """Personal user account where he can edit user data"""
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile)
            if int(request.POST['age']) < 18:
                return render(request, 'user/user_account.html',
                              {'error': 'Your age must be at least 18 years old'})
            elif not str(request.POST['age']).isnumeric():
                return render(request, 'user/user_account.html', {'error': 'Incorrect age field'})
            else:
                try:
                    u_form.save()
                    p_form.save()
                    return redirect('user_app:user_account')  # Перенаправление на страницу профиля пользователя
                except ValueError:
                    return render(request, 'user/user_account.html',
                                  {'error': 'Files is too large, requirement is less than 2.5 MB'})

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'favorites': Favorite.objects.filter(user=request.user).order_by('-saved_date')
        }

        return render(request, 'user/user_account.html', context)

    return redirect('user_app:sign_up_step_three')


def signin(request):
    """Вход пользователя"""
    if request.user.is_authenticated:  # Если пользователь в системе, то у него нет доступа к форме входа
        return redirect('dating_app:dating')
    else:
        if request.method == 'GET':
            return render(request, 'user_app/sign_in.html',
                          {'form': AuthenticationForm()})
        else:
            user = authenticate(request, username=request.POST['username'],
                                password=request.POST['password'])
            if user is None:
                return render(request, 'user_app/sign_in.html',
                              {'form': AuthenticationForm(),
                               'error_signin': 'Username or password did not match'})
            else:
                login(request, user)
                return redirect('dating_app:dating')


@login_required
def sign_up_step_three(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.city and profile.sex and profile.seeking:
        if request.method == 'POST':
            step_three_form = SignUpStepThreeForm(request.POST,
                                                  request.FILES,
                                                  instance=request.user.profile)
            if not (request.POST['about']):
                return render(request, 'user/sign_up_step_three.html', {'error': 'About field can\'t be empty'})
            else:
                try:
                    step_three_form.save()
                    return redirect('dating_app:dating')
                except ValueError:
                    return render(request, 'user/sign_up_step_three.html',
                                  {'error': 'File is too large, requirement is less than 2.5 MB'})

        else:
            step_three_form = SignUpStepThreeForm(instance=request.user.profile)

        context = {
            'step_three_form': step_three_form,
        }
        return render(request, 'user/sign_up_step_three.html', context)
    return redirect('user_app:sign_up_step_two')
