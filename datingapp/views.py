from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from userapp.models import Profile


# Create your views here.
@login_required
def home(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.about:
        return redirect('dating_app:dating')
    return redirect('user_app:sign_up_step_three')
