from django.shortcuts import redirect
from rest_framework import status

from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from analytics.searchs import TagSearch
from analytics.serializers import TagSerializer, BannerSerializer, NotificationSerializer, UserActionSerializer
from analytics.models import Banner, UserAction
from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet, PermissionModelViewSet


class TagViewSet(PermissionReadOnlyModelViewSet):
    search_class = TagSearch
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class BannerViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = BannerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Banner.active_banners()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj = obj.clicked()
        link = obj.get_redirect_url(request=request)
        if link:
            return redirect(to=link)
        return Response()


class NotificationViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return self.request.user.events.all()


class UserActionViewSet(PermissionModelViewSet):
    serializer_class = UserActionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return self.request.user.actions.all()

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            data_list = request.data
            for data in data_list:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return super(UserActionViewSet, self).create(request, args, kwargs)
