
from django.forms import ValidationError
from django.db import IntegrityError
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import UserData, MatchModel

class UserRegistrationSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('email','first_name','last_name','city','image','male_type','password')

class MatchSerializers(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = MatchModel
        fields = ('sender',)
    
    def validate(self, artts):
        if self.context['sender_2'] == artts['sender']:
            raise ValidationError('Ошибка')
        return artts
    
    def create(self, validated_data):
        try:
            return MatchModel.objects.create(sender=validated_data['sender'],
                                        sender_2=self.context['sender_2'])
        except IntegrityError:
            raise ValidationError('Вы уже отправили ему.')
    

class ListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('id','first_name','last_name','image','male_type')
        