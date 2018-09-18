from rest_framework import generics

from .models import Item
from .permissions import AllowOptionsAuthentication
from .serializers import ItemSerializer


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowOptionsAuthentication]


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowOptionsAuthentication]


class CreateGroupView():
    pass
