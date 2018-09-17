from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import generics

from .models import Item
from .permissions import AllowOptionsAuthentication
from .serializers import ItemSerializer


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [AllowOptionsAuthentication]


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [AllowOptionsAuthentication]
