import django_filters
from django_filters import FilterSet
from django.utils.translation import gettext_lazy as _
from board.models import Reply, Post

class ReplyFilter(FilterSet):
    class Meta:
        model = Post
        fields = ['title', ]
        labels = {'title': _('Обьявление')}