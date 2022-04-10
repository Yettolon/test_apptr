import math
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from geopy.geocoders import Nominatim
from django.db.models.signals import post_save
from django.dispatch import receiver

from imagekit.models import ProcessedImageField
from .utilites import timestapppp, Waters


class UserDataManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,image,password,male_type,city):
        geolocator = Nominatim(user_agent=first_name)
        location = geolocator.geocode(city)
        user = self.model(email=email, first_name=first_name,
                        last_name=last_name, image=image,password=password, male_type=male_type,
                        city=city,latitude=location.latitude,longitude=location.longitude)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using = self._db)
        return user

    def create_superuser(self,email,first_name,last_name,image ,password,city):
        geolocator = Nominatim(user_agent=first_name)
        location = geolocator.geocode(city)
        user = self.create_user(email=email,first_name=first_name,
                        last_name=last_name,password=password,image=image,
                        male_type=1,city=city)

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self,email_):
        print(email_)
        return self.get(email=email_)


class UserData(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name='Имя', max_length=100, blank=False)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100, blank=False)
    email = models.EmailField(verbose_name='Электронная почта', unique=True, blank=False,)
    image = ProcessedImageField(blank=False, verbose_name='Аватар',
                            upload_to=timestapppp, processors=[Waters()])
    latitude =  models.FloatField(verbose_name='Долгота',default=0)
    longitude = models.FloatField(verbose_name='Широта',default=0)
    MALES = (
        (1, 'Мужской'),
        (2, 'Женский'),
    )
    male_type = models.IntegerField(verbose_name='Пол', choices=MALES, default=1)

    city = models.CharField(max_length=100,verbose_name='City', default='Moscow')
    is_staff = models.BooleanField(default=False)
    geo_data = models.ManyToManyField('GeoModel',)
    REQUIRED_FIELDS = ['first_name','last_name','image','city']
    USERNAME_FIELD = 'email'

    objects = UserDataManager()

    def get_short_name(self):
        return self.first_name
    
    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name='User'
        verbose_name_plural = 'Users'
        ordering = ('email',)

class MatchModel(models.Model):
    sender = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='sender')
    sender_2 = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='sender_2')

    class Meta:
        unique_together = ('sender','sender_2')


class GeoModel(models.Model):
    geo = models.FloatField(default=0)
    user = models.CharField(max_length=400,default=None)
    user2 = models.CharField(max_length=400,default=None)

    class Meta:
        unique_together = ('user','user2') 
    
    
    


def get_distance_between_users(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    length = 2 * math.asin(math.sqrt(math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2))
    km = 6371 * length
    return round(km, 3)

@receiver(post_save, sender=UserData)
def sign(sender, instance, **kwargs):
    x = UserData.objects.all().values('longitude','latitude','id')
    geolocator = Nominatim(user_agent=instance.first_name)
    location = geolocator.geocode(instance.city)
    for i in x:
        if i.get('id')!=instance.id: 
            z = get_distance_between_users(i.get('longitude'),i.get('latitude'),
                                            location.longitude,location.latitude)
            GeoModel.objects.create(geo=z,user=instance.id,
                                    user2=i.get('id'))
            GeoModel.objects.create(geo=z,user2=instance.id,
                                    user=i.get('id'))
    
