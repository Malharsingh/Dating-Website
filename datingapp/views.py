from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import redirect

from userapp.models import Profile


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
