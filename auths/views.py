from django.shortcuts import render,reverse,HttpResponseRedirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm,LoginForm,UserProfileUpdateForm,UserPasswordChangeForm2
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from following.models import Following

from django.contrib.auth.decorators import login_required
from blog.decorators import anonymous_required
from .models import UserProfile
from blog.models import Blog

# Create your views here.

@anonymous_required
def register(request):
    if not request.user.is_anonymous:
        return HttpResponseRedirect(reverse("posts:list"))
    #if request.user.is_authenticated:
    #   return HttpResponseRedirect(reverse("post:list"))

    form = RegisterForm(data = request.POST or None)
    if form.is_valid():
        user = form.save(commit = False)
        password = form.cleaned_data.get("password")
        username = form.cleaned_data.get("username")
        user.set_password(password)
        user.save()
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                messages.success(request,"<b>Tebrikler kaydınız başarıyla gerçekleşti.</b>",extra_tags = "success")
                return HttpResponseRedirect(user.userprofile.get_user_profile_url())
    return  render(request, 'auths/register.html', context = {"form":form})

@anonymous_required
def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                msg = "<b>Merhaba %s Sisteme Hoşgeldiniz.</b>"%(username)
                messages.success(request,msg , extra_tags="success")
                return HttpResponseRedirect(reverse("posts:list"))
    return render(request,"auths/login.html" ,context = {"form": form})


def user_logout(request):
    username = request.user.username
    logout(request)
    msg = "<b>Sistemden Çıkış Yaptınız {}  </b>".format(username)
    messages.success(request,msg,extra_tags = "success")
    return HttpResponseRedirect(reverse("auths:login"))

def user_profile(request,username):
    takip_ediyor_mu = False
    user = get_object_or_404(User, username = username)
    blog_list = Blog.objects.filter(user = user)
    takipci_ve_takip_edilen = Following.kullanici_takiplesme_tablosu(user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    #eğer kendi profiline girmişse fonksiyon gereksiz çalışmasın diye
    if user != request.user:
        takip_ediyor_mu = Following.kullanici_takip_kontrol(follower = request.user, followed = user)
    return render(request,"auths/profile/userprofile.html",
                  context = {'takipciler':takipciler, 'takip_edilenler':takip_edilenler, "takip_ediyor_mu":takip_ediyor_mu, "user": user, "blog_list":blog_list, 'page': 'user_profile'})

def user_settings(request):
    sex = request.user.userprofile.sex
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    dogum_tarihi = request.user.userprofile.dogum_tarihi

    takipci_ve_takip_edilen = Following.kullanici_takiplesme_tablosu(request.user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    initial = {'sex' : sex, 'bio' : bio, 'profile_photo' : profile_photo, "dogum_tarihi": dogum_tarihi}
    form = UserProfileUpdateForm(initial = initial, instance = request.user, data = request.POST or None, files = request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit = True)
            bio = form.cleaned_data.get('bio',None)
            sex = form.cleaned_data.get('sex',None)
            dogum_tarihi = form.cleaned_data.get("dogum_tarihi",None)
            profile_photo = form.cleaned_data.get('profile_photo',None)

            user.userprofile.bio = bio
            user.userprofile.sex = sex
            user.userprofile.dogum_tarihi = dogum_tarihi
            user.userprofile.profile_photo = profile_photo
            user.userprofile.save()
            messages.success(request,"Tebrikler Kullanıcı Bilgileriniz Başarıyla Güncellendi.",extra_tags = "success")
            return HttpResponseRedirect(reverse('auths:user_profile', kwargs = {'username': user.username}))
        else:
            messages.warning(request,"Lütfen Form Alanlarına Doğru Giriniz.",extra_tags = "danger")
    return render(request, "auths/profile/settings.html", context={'takipciler':takipciler,
                                            'takip_edilenler':takip_edilenler, "form": form, 'page': 'settings'})

def user_password_change(request):
    form = UserPasswordChangeForm2(user = request.user, data = request.POST or None)
    takipci_ve_takip_edilen = Following.kullanici_takiplesme_tablosu(request.user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    if form.is_valid():
        user = form.save(commit = True)
        update_session_auth_hash(request, user)
        messages.success(request,"Tebrikler Şifreniz Başarıyla Güncellendi.")
        return HttpResponseRedirect(reverse('auths:user_profile',kwargs = {"username": request.user.username}))
    return render(request,"auths/profile/password_change.html", context = {'takipciler':takipciler,
                                            'takip_edilenler':takip_edilenler,"form": form, 'page': 'password_change'})

def user_about(request,username):
    takip_ediyor_mu = False
    user = get_object_or_404(User, username = username)
    takipci_ve_takip_edilen = Following.kullanici_takiplesme_tablosu(user)
    takipciler = takipci_ve_takip_edilen['takipciler']
    takip_edilenler = takipci_ve_takip_edilen['takip_edilenler']

    # eğer kendi profiline girmişse fonksiyon gereksiz çalışmasın diye
    if user != request.user:
        takip_ediyor_mu = Following.kullanici_takip_kontrol(follower=request.user, followed=user)

    return render(request,"auths/profile/about_me.html",
                  context = {'takipciler':takipciler, 'takip_edilenler':takip_edilenler,
                                                 "takip_ediyor_mu":takip_ediyor_mu, "user": user, "page":"about"})

