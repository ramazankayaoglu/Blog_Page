from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest,JsonResponse
from django.shortcuts import get_object_or_404,Http404
from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage

from .models import Following

def kullanici_modal_takip_et_cikar(request):
    response = sub_kullanici_takip_et_cikar(request)
    follow_type = request.GET.get('follow_type')
    owner = request.GET.get('owner')
    data = response.get('data')
    #followed = response.get('followed')
    #kendi profilimmiş gibi hareket ediyorum ve kendi takipçilerimi tekrardan çekiyorum.
    my_followed = Following.get_followed_username(user = request.user)

    if owner == request.user.username:
        takipci_ve_takip_edilen_sayısı = Following.kullanici_takiplesme_tablosu(request.user)

        context = {'user': request.user, 'takipciler': takipci_ve_takip_edilen_sayısı['takipciler'],
                   'takip_edilenler': takipci_ve_takip_edilen_sayısı['takip_edilenler']}

        html_render_takip_durum = render_to_string('auths/profile/include/following/following_partion.html', context=context,
                                request=request)
        if follow_type == 'followed':
            following = Following.get_followed(user=request.user)
            following = followers_and_followed_paginate(following,1)
            html = render_to_string('following/profile/include/following_followed_list.html', context={
                'following': following, 'my_followed': my_followed, 'follow_type': follow_type}, request=request)
            html_paginate = render_to_string("following/profile/include/button_include/show_more_button.html", context=
            {'following': following, 'follow_type': follow_type, 'username': request.user.username})

            data.update({ 'html':html,'html_paginate':html_paginate})

        data.update({'follow_type':follow_type, 'html_render_takip_durum':html_render_takip_durum, 'owner':True})
    else:
        data.update({'owner': False})
    return JsonResponse(data = data)


def kullanici_takip_et_cikar(request):

    response = sub_kullanici_takip_et_cikar(request)
    data = response.get('data')
    followed = response.get('followed')
    takipci_ve_takip_edilen_sayısı = Following.kullanici_takiplesme_tablosu(followed)
    context = {'user':followed, 'takipciler':takipci_ve_takip_edilen_sayısı['takipciler'],
               'takip_edilenler':takipci_ve_takip_edilen_sayısı['takip_edilenler']}
    html = render_to_string('auths/profile/include/following/following_partion.html',context = context, request = request)
    data.update({'html': html})
    return JsonResponse(data = data)

def kullanici_takip_et_cikar_for_post(request):
    data = {'html': ''}
    response = sub_kullanici_takip_et_cikar(request)
    takip_edilen_kullanici = response.get('followed')
    my_followed_user = Following.get_followed_username(request.user)

    html = render_to_string('blog/include/favorite/favorite_user_obj.html', context = {'user': takip_edilen_kullanici,
                   'my_followed_user':my_followed_user }, request = request )
    data.update({'html':html})
    return JsonResponse(data = data)

def sub_kullanici_takip_et_cikar(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()

    data = {'takip_durum': True, 'html':'', "is_valid": True,'msg':'<b>Takibi Bırak</b>'}
    follower_username = request.GET.get('follower_username',None)
    followed_username = request.GET.get('followed_username',None)

    follower = get_object_or_404(User, username = follower_username)
    followed = get_object_or_404(User, username = followed_username)

    takip_ediyor_mu = Following.kullanici_takip_kontrol(follower = follower, followed = followed)

    if not takip_ediyor_mu:
        Following.kullanici_takip_et(follower = follower, followed = followed)
    else:
        Following.kullanici_takipten_cikar(follower = follower, followed = followed)
        data.update({'msg':'<b>Takip Et</b>', 'takip_durum':False})
    return {'data':data, 'followed':followed}


def ramo(request):
    return render(request,"following/ramo.html")



def followed_or_followers_list(request,follow_type):
    data = {'is_valid':True,'html':''}
    page = request.GET.get('page',1)
    username = request.GET.get('username',None)
    if not username:
        raise Http404
    user = get_object_or_404(User,username = username)
    my_followed = Following.get_followed_username(user = request.user)

    if follow_type == 'followed':
        takip_edilenler = Following.get_followed(user = user)
        takip_edilenler = followers_and_followed_paginate(queryset = takip_edilenler, page = page )
        html = render_to_string('following/profile/include/following_followed_list.html',context = {'following' :takip_edilenler,
                                    'my_followed' : my_followed, 'follow_type':follow_type}, request = request)

        html_paginate = render_to_string("following/profile/include/button_include/show_more_button.html",context =
        {'following':takip_edilenler, 'follow_type':follow_type, 'username': user.username})

        #kullanıcının takip ettiği kişiler.
    elif follow_type == 'followers':
        takipciler = Following.get_followers(user = user)
        takipciler = followers_and_followed_paginate(queryset = takipciler, page = page)
        html = render_to_string('following/profile/include/following_followed_list.html',
                                context = {'following' : takipciler, 'my_followed' : my_followed,
                                         'follow_type':follow_type}, request = request)
        html_paginate = render_to_string('following/profile/include/button_include/show_more_button.html',
                                         context = {'following':takipciler, 'follow_type':follow_type,'username':user.username})
        #kullanıcıyı takip eden kişiler.
    else:
        raise Http404
    data.update({'html':html, 'html_paginate':html_paginate})
    return JsonResponse(data = data)


def followers_and_followed_paginate(queryset,page):
    paginator = Paginator(queryset,1)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return queryset