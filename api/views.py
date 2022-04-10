import django_filters
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from djoser.views import UserViewSet

from django.core.mail import send_mail
from django.template.loader import render_to_string


from .serializers import MatchSerializers, ListSerializers
from .models import GeoModel, UserData, MatchModel
from sit.settings import DEFAULT_FROM_EMAIL
from .service import ListFilter

class UserViewSets(UserViewSet):
    permission_classes=[AllowAny]


class MatchView(ModelViewSet):
    serializer_class = MatchSerializers
    permission_classes = [IsAuthenticated]
    queryset = MatchModel.objects.all()
    http_method_names = ['post']

    @action(name='math_sender',detail=True,method=['POST'])
    def match(self, request, pk):
        sender = request.user
        sender_2 = UserData.objects.get(pk=pk)
        serializerss = MatchSerializers(context={'sender_2': sender_2,
                                    'request': request}, data=request.data)
        valid = serializerss.is_valid(raise_exception=True)
        if valid:
            serializerss.save()
        mat = MatchModel.objects.filter(sender=sender_2,sender_2=sender)
        if mat:
            context = {'sender':sender,'sender_2':sender_2}
            sub = render_to_string('email/send_sub.txt',context)
            body = render_to_string('email/send_bod.txt',context)
            send_mail(sub,body,DEFAULT_FROM_EMAIL,[sender.email],fail_silently=False)
            sub2 = render_to_string('email/send_sub2.txt',context)
            body2 = render_to_string('email/send_bod2.txt',context)
            send_mail(sub2,body2,DEFAULT_FROM_EMAIL,[sender_2.email],fail_silently=False)
            return Response(sender_2.email, 201)
        else:
            return Response(f'Вот его почта {sender_2.first_name}.', 201)

class ListView(generics.ListAPIView):
    
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    queryset = UserData.objects.all()
    serializer_class = ListSerializers
    filterset_class = ListFilter

    def get_queryset(self):
        try:
            distance = self.request.GET.get('geo_range')
            geo_users = GeoModel.objects.filter(user=self.request.user.id)
            x = geo_users.filter(geo__lte=distance)
            id_users = []
            for i in x:
                id_users.append(i.user2)
            y = tuple(id_users)
            queryset = UserData.objects.filter(id__in=y)
            return queryset
        except ValueError:
            queryset = UserData.objects.all()
            return queryset
        except TypeError:
            queryset = UserData.objects.all()
            return queryset
        



