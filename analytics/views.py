
from rest_framework.decorators import list_route, detail_route
from analytics.models import Like, Favorite
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status
from karaoke.models import Post
from rest_framework.permissions import IsAuthenticated
from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.models import User
from loginapp.serializers import UserProfileSerializer
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet
from musikhar.utils import Errors


class LikeViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return User.objects.none()

    @list_route
    def get_like(self, request):

        return self.do_pagination(queryset=request.user.get_like())


    @list_route(methods=['post'])
    def like(self, request):
        data = request.data
        liked = data.get('like')
        liked_user = data.get('user')
        liked_post = data.get('post')

        if liked:
            try:
                like_user = User.objects.get(username=liked_user)
                like_post = Post.objects.get(name=liked_post)
                Like.objects.create(post=like_post, user=like_user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                errors = Errors.get_errors(Errors, error_list=['User_Not_Found'])
                return Response(data=errors, status=status.HTTP_404_NOT_FOUND)

        errors = Errors.get_errors(Errors, error_list=['Missing_Form'])
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return User.objects.none()

    @list_route
    def full(self, request):
        return self.do_pagination(queryset=request.user.get_favorite())
