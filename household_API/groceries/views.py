from django.contrib.auth.models import Group
from rest_framework import generics

from .models import Item
from .permissions import AllowOptionsAuthentication
from .serializers import ItemSerializer, GroupSerializer


class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [AllowOptionsAuthentication]

    def get_queryset(self):
        try:
            qs = Item.objects.filter(group=self.request.user.groups.first().id)
        except AttributeError:
            qs = list()
        return qs


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [AllowOptionsAuthentication]

    def get_queryset(self):
        try:
            qs = Item.objects.filter(group=self.request.user.groups.first().id)
        except AttributeError:
            qs = list()
        return qs


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowOptionsAuthentication]


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowOptionsAuthentication]
