from django.db import models
from django.contrib.auth.models import User


class Following(models.Model):
    follower = models.ForeignKey(User, related_name = "follower", null = True, verbose_name = "Takip Eden Kullanıcı", on_delete = models.PROTECT)
    followed = models.ForeignKey(User, related_name = "following", null = True, verbose_name = "Takip Edilen Kullanıcı", on_delete = models.PROTECT)

    class Meta:
        verbose_name_plural = "Takipleşme Sistemi"

    def __str__(self):
        return "Follower {} - Followed {}".format(self.follower.username,self.followed)

    @classmethod
    def kullanici_takip_et(cls,follower,followed):
        cls.objects.create(follower = follower, followed = followed)

    @classmethod
    def kullanici_takipten_cikar(cls,follower,followed):
        cls.objects.filter(follower = follower, followed = followed).delete()

    @classmethod
    def kullanici_takip_kontrol(cls,follower,followed):
        return cls.objects.filter(follower = follower, followed = followed).exists()

    @classmethod
    def kullanici_takiplesme_tablosu(cls,user):
        data = {'takip_edilenler':0, 'takipciler':0}
        takip_edilenler = cls.objects.filter(follower = user).count()
        takipciler = cls.objects.filter(followed = user).count()

        data.update({'takip_edilenler':takip_edilenler, 'takipciler':takipciler})
        return data

    @classmethod
    def get_followers(cls,user):
        return cls.objects.filter(followed = user)
            #kullanıcının takip ettiklerini getir.

    @classmethod
    def get_followed(cls, user):
        return cls.objects.filter(follower = user)
        #kullanıcıyı takip edenleri getir..

    @classmethod
    def get_followed_username(cls,user):
        followed = cls.get_followed(user)
        yanit = followed.values_list('followed__username',flat = True)
        return yanit