from django.contrib.auth.models import Group
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        # Save the request data
        data = request.data
        # Add the id of the user's group to the data before saving to db
        data['group'] = request.user.groups.first().id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            # Grabs the 'name' parameter from the URL
            obj = queryset.get(name=self.kwargs['name'])
            obj.user_set.add(self.request.user)
        except Group.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj
