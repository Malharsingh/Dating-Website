import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from userapp.models import Profile
from .models import Favorite

favorite_user = list()


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
            Q(first_name__startswith=query) | Q(last_name__startswith=query), sex__in=sex
        ).exclude(id=request.user.id)

        context = get_pagination(request, profiles_list, 10)
        if profiles_list:
            context.update({'query': f'We found {len(profiles_list)} people with name "{query}"'})
            context.update({'saved_to_favorite': Favorite.objects.values_list('saved', flat=True)})
            context.update({'favorites': Favorite.objects.filter(user=request.user).order_by('-saved_date')})
        else:
            context.update({'query': f'There are no people with name "{query}"'})
        return render(request, 'datingapp/dating.html', context)
    return redirect('userapp:sign_up_step_three')


def favorite_add(request, user_id):
    saved = User.objects.get(id=user_id)
    favorites = Favorite.objects.filter(user=request.user, saved=saved)
    if not favorites.exists():
        Favorite.objects.create(user=request.user, saved=saved)
        favorites_count = request.session.get('favorites_count', 0) + 1
        request.session['favorites_count'] = favorites_count
        favorite_user.append(saved.id)
        request.session['favorites'] = favorite_user
    else:
        favorite = favorites.first()
        favorite.delete()
        favorites_count = request.session.get('favorites_count', 0)
        if favorites_count > 0:
            request.session['favorites_count'] = favorites_count - 1
    response = HttpResponseRedirect(request.META['HTTP_REFERER'])
    response.set_cookie('favorites_count', str(request.session.get('favorites_count', 0)))
    response.set_cookie('favorites', request.session.get('favorites', 0))
    return response


@login_required
def partner_account(request, user_id):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.about:
        """Show profile details of other users"""
        partner_account = get_object_or_404(User, pk=user_id)
        return render(request, 'datingapp/partner_account.html', {'partner_account': partner_account,
                                                                  'favorites': Favorite.objects.filter(
                                                                      user=request.user).order_by('-saved_date')})
    return redirect('userapp:sign_up_step_three')


# Create your views here.
@login_required
def home(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.about:
        return redirect('datingapp:dating')
    return redirect('userapp:sign_up_step_three')


def get_pagination(request, profiles_list, objects_num):
    """Pagination"""
    paginator = Paginator(profiles_list, objects_num)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        cards = paginator.page(page)
    except(EmptyPage, InvalidPage):
        cards = paginator.page(paginator.num_pages)
    page_range = paginator.get_elided_page_range(number=page)

    context = {
        'cards': cards,
        'page_range': page_range
    }
    return context


def random_card(request):
    profile = Profile.objects.get(pk=request.user.pk)
    card_list = list(Profile.objects.filter(sex__in=str(profile.seeking)
                                            ).exclude(id=request.user.id))
    if card_list:
        random_card = random.sample(card_list, 1)
    else:
        random_card = None

    # Initialize favorites and skips count in cookies if not already set
    favorites_count = request.session.get('favorites_count', 0)
    skips_count = request.session.get('skips_count', 0)
    response = render(request, 'datingapp/random_card.html', {'random_card': random_card,
                                                              'favorites': Favorite.objects.filter(
                                                                  user=request.user).order_by(
                                                                  '-saved_date'), 'favorites_count': favorites_count,
                                                              'skips_count': skips_count})
    response.set_cookie('favorites_count', str(favorites_count))
    response.set_cookie('skips_count', str(skips_count))
    return response
