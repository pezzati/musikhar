from django.shortcuts import redirect

from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from analytics.searchs import TagSearch
from analytics.serializers import TagSerializer, BannerSerializer, NotificationSerializer
from analytics.models import Banner
from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet


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