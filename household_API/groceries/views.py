from django.contrib.auth.hashers import check_password, make_password
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
        serializer = self.get_serializer(data=data)
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

    def create(self, request, *args, **kwargs):
        data = dict()
        data['name'] = request.data['name']
        data['password'] = make_password(request.data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        group = Group.objects.get(name=data['name'])
        group.user_set.add(request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowOptionsAuthentication]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            # Grabs the 'name' parameter from the URL
            group = queryset.get(name=self.kwargs['name'])
        except Group.DoesNotExist:
            raise Http404
        if not check_password(self.request.data['password'], group.password):
            raise Http404

        self.check_object_permissions(self.request, group)
        return group

    def update(self, request, *args, **kwargs):
        group = self.get_object()

        queryset = self.filter_queryset(self.get_queryset())

        if not check_password(request.data['password'], group.password):
            raise Http404

        data = {
            'name': request.data['name'],
            'password': group.password,
        }

        serializer = self.get_serializer(group, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        group.user_set.add(self.request.user)

        if getattr(group, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            group._prefetched_objects_cache = {}

        return Response(serializer.data)
