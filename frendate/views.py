from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
#from .models import Favorite
import random


@login_required
def dating(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.about:
        """Search for users"""
        query = request.GET.get("q", default="")
        sex = request.GET.get('sex', default="ALL")
        if sex == 'ALL':
            sex = ['M', 'F']

        profiles_list = Profile.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query), sex__in=sex
        ).exclude(id=request.user.id)

        #context = get_pagination(request, profiles_list, 10)
        if profiles_list:
            context.update({'query': f'We found {len(profiles_list)} people with name "{query}"'})
            #context.update({'saved_to_favorite': Favorite.objects.values_list('saved', flat=True)})
            #context.update({'favorites': Favorite.objects.filter(user=request.user).order_by('-saved_date')})
        else:
            context.update({'query': f'There are no people with name "{query}"'})
        return render(request, 'dating_app/dating.html', context)
    return redirect('user_app:sign_up_step_three')