from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route

from rest_framework.permissions import IsAuthenticated

from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.models import User
from loginapp.serializers import UserProfileSerializer

from musikhar.abstractions.views import PermissionReadOnlyModelViewSet


class LikeViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return User.objects.none()

    @list_route()
    def like_get(self, request):
        liked = request.like.user_set.all()
        return self.do_pagination(queryset=liked)


class FavoriteViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return User.objects.none()

    @list_route()
    def favorite_get(self, request):
        favored = request.favorite.user_set.all()
        return self.do_pagination(queryset=favored)
