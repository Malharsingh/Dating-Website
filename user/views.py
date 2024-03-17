from django.db import models
from django.shortcuts import render, redirect

from djangoProject.user_app.forms import SignUpStepOneForm


# Create your views here.
def signup_one(request):
	if request.method == 'POST':
		step_one_form = SignUpStepOneForm(request.POST,request.FILES, instance=request.user.profile)

		if not(request.POST['first_name']):
			return render(request, 'user_app/signup_one.html', {'error': 'First name can\'t be empty'})
		if not(str(request.POST['first_name']).isalpha()):
			return render(request, 'user_app/signup_one.html', {'error': 'First name can\'t have numbers'})
		elif not(request.POST['last_name']):
			return render(request, 'user_app/signup_one.html', {'error': 'Last name can\'t be empty'})
		if not(str(request.POST['last_name']).isalpha()):
			return render(request, 'user_app/signup_one.html', {'error': 'Last name can\'t have numbers'})
		elif not(request.POST['age']):
			return render(request, 'user_app/signup_one.html', {'error': 'Age can\'t be empty'})
		elif int(request.POST['age']) < 18:
			return render(request, 'user_app/signup_one.html', {'error': 'Your age must be at least 18 years old'})
		elif not str(request.POST['age']).isnumeric():
				return render(request, 'user_app/signup_one.html', {'error':'Uncorrect age field'})
		else:
			step_one_form.save()
			return redirect('user_app:signup_two')
	else:
		step_one_form = SignUpStepOneForm(instance=request.user.profile)

	context = {
		'step_one_form': step_one_form,
	}
	return render(request, 'user_app/signup_one.html', context)


@login_required
def user_account(request):
	profile = Profile.objects.get(pk=request.user.pk)
	if profile.about:
		"""Личный аккаунт пользователя, где он может редактировать пользовательские данные"""
		if request.method == 'POST':
			u_form = UserUpdateForm(request.POST, instance=request.user)
			p_form = ProfileUpdateForm(request.POST,
									   request.FILES,
									   instance=request.user.profile)
			if int(request.POST['age']) < 18:
				return render(request, 'user_app/user_account.html',
							  {'error': 'Your age must be at least 18 years old'})
			elif not str(request.POST['age']).isnumeric():
				return render(request, 'user_app/user_account.html', {'error': 'Uncorrect age field'})
			else:
				try:
					u_form.save()
					p_form.save()
					return redirect('user_app:user_account')  # Перенаправление на страницу профиля пользователя
				except ValueError:
					return render(request, 'user_app/user_account.html',
								  {'error': 'Files is too large, requirement is less than 2.5 MB'})

		else:
			u_form = UserUpdateForm(instance=request.user)
			p_form = ProfileUpdateForm(instance=request.user.profile)

		context = {
			'u_form': u_form,
			'p_form': p_form,
			'favorites': Favorite.objects.filter(user=request.user).order_by('-saved_date')
		}

		return render(request, 'user_app/user_account.html', context)

	return redirect('user_app:sign_up_step_three')