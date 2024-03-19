import random
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import get_object_or_404, redirect, render

from userapp.models import Profile

@login_required
def partner_account(request, user_id):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.about:
        """Show profile details of other users"""
        partner_account = get_object_or_404(User, pk=user_id)
        return render(request, 'dating_app/partner_account.html', {'partner_account': partner_account,
                                                                   'favorites': Favorite.objects.filter(
                                                                       user=request.user).order_by('-saved_date')})
    return redirect('user_app:sign_up_step_three')


# Create your views here.
@login_required
def home(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.about:
        return redirect('dating_app:dating')
    return redirect('user_app:sign_up_step_three')


def get_pagination(request, profiles_list, objects_num):
    """Pagination"""
    paginator = Paginator(profiles_list, objects_num)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        cards = paginator.page(page)
    except (EmptyPage, InvalidPage):
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
    return render(request, 'dating_app/random_card.html', {'random_card': random_card,
                                                           'favorites': Favorite.objects.filter(
                                                               user=request.user).order_by('-saved_date')})




