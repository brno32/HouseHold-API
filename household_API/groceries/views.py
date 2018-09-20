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
        return Item.objects.filter(group=self.request.user.groups.first().id)


class GroupList(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [AllowOptionsAuthentication]
