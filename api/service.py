from django_filters import rest_framework as filters

from .models import UserData


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class ListFilter(filters.FilterSet):
    first_name = CharFilterInFilter(field_name='first_name', lookup_expr='in')
    last_name = CharFilterInFilter(field_name='last_name', lookup_expr='in')




    class Meta:
        model = UserData
        fields = ('first_name','last_name','male_type')

