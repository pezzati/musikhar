from django.shortcuts import redirect

from rest_framework.decorators import detail_route
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from analytics.searchs import TagSearch
from analytics.serializers import TagSerializer, BannerSerializer
from analytics.models import Like, Favorite, Banner
from karaoke.models import Post
from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet
from musikhar.utils import Errors
from analytics.serializers import LikeSerializer, FavoriteSerializer


class LikeViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Like.objects.none()

    @detail_route()
    def full(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Info'])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return self.do_pagination(queryset=post.like_set.all())

    @detail_route(methods=['post'])
    def like(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Info'])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        Like.objects.get_or_create(user=request.user, post=post)

        return Response(status=status.HTTP_201_CREATED)


class FavoriteViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return self.request.user.favorite_set.all()

    @detail_route(methods=['post'])
    def favorite(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Info'])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.get_or_create(user=request.user, post=post)

        return Response(status=status.HTTP_201_CREATED)


class TagViewSet(PermissionReadOnlyModelViewSet):
    search_class = TagSearch
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BannerViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = BannerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        return Banner.active_banners()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj = obj.clicked()
        link = obj.get_redirect_url(request=request)
        if link:
            return redirect(to=link)
        return Response()
