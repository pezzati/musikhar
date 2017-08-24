from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.models import User, Follow
from loginapp.serializers import UserProfileSerializer
from loginapp.forms import ProfileForm
from musikhar.abstractions.messages import ErrorMessaging
from musikhar.abstractions.views import IgnoreCsrfAPIView, PermissionReadOnlyModelViewSet


class ProfileView(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        form = ProfileForm(data)
        if form.is_valid():
            user = request.user
            serializer = UserProfileSerializer(instance=user)
            serializer.update(instance=user, validated_data=form.cleaned_data)
            return Response(data=serializer.data)

        errors = ErrorMessaging()
        errors = errors.get_errors(error_list=form.error_translator())
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = UserProfileSerializer(instance=request.user)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)


class FollowingViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return User.objects.none()

    @list_route()
    def followings(self, request):
        followings = request.user.get_following()
        return self.do_pagination(queryset=followings)

    @list_route()
    def followers(self, request):
        followers = request.user.get_followers()
        return self.do_pagination(queryset=followers)

    @list_route(methods=['post'])
    def follow(self, request):
        data = request.data
        followed = data.get('followed')
        if followed:
            try:
                followed_user = User.objects.get(username=followed)
                Follow.objects.create(followed=followed_user, follower=request.user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # TODO error msg
                return Response(status=status.HTTP_404_NOT_FOUND)

        # TODO error msg
        return Response(status=status.HTTP_400_BAD_REQUEST)

