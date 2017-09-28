
from rest_framework.decorators import detail_route
from analytics.models import Like, Favorite
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from karaoke.models import Post
from rest_framework.permissions import IsAuthenticated
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
