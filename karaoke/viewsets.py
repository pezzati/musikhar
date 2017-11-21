from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from analytics.models import UserFileHistory, Like, Favorite
from karaoke.searchs import PostSearch, GenreSearch
from karaoke.serializers import SongSerializer, GenreSerializer, PoemSerializer, PostSerializer, KaraokeSerializer
from karaoke.models import Song, Genre, Poem, Post
from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.serializers import UserInfoSerializer
from mediafiles.models import MediaFile
from musikhar.abstractions.exceptions import NoFileInPost
from musikhar.abstractions.views import PermissionModelViewSet, PermissionReadOnlyModelViewSet
from musikhar.utils import Errors


class PostViewSet(PermissionModelViewSet):
    serializer_class = PostSerializer
    search_class = PostSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Post.objects.all()

    def check_object_permissions(self, request, obj):
        if obj.user_has_access(request.user):
            pass
        else:
            raise PermissionDenied

    @detail_route(methods=['get'], permission_classes=())
    def file(self, request, pk):
        try:
            target_post = Post.objects.get(id=pk)
            target_file = target_post.get_file()
        except Post.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Info'])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        except NoFileInPost:
            errors = Errors.get_errors(Errors, error_list=[NoFileInPost.error_msg_key])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request=request, obj=target_post)

        redirect, uri = target_file.get_download_path()
        if request.user.is_authenticated():
            UserFileHistory.objects.create(requested_user=request.user,
                                           post=target_post)
        else:
            UserFileHistory.objects.create(post=target_post)
        if not redirect:
            content_type = target_file.get_content_type()
            response = HttpResponse()
            response['Content-Type'] = content_type
            response['X-Accel-Redirect'] = uri
            return response
        else:
            return redirect(to=uri)

    @detail_route(methods=['post', 'get', 'delete'])
    def like(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Info'])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            Like.objects.get_or_create(user=request.user, post=post)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'GET':
            return self.do_pagination(queryset=post.likes.all(), serializer_class=UserInfoSerializer)
        elif request.method == 'DELETE':
            try:
                Like.objects.get(user=request.user, post=post).delete()
            except Like.DoesNotExist:
                pass
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @detail_route(methods=['post', 'delete'])
    def favorite(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Info'])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            Favorite.objects.get_or_create(user=request.user, post=post)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            try:
                Favorite.objects.get(user=request.user, post=post).delete()
            except Favorite.DoesNotExist:
                pass
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SongViewSet(PermissionModelViewSet):
    serializer_class = PostSerializer
    search_class = PostSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @silk_profile(name='View Songs')
    def get_queryset(self):
        return Post.objects.filter(subclass_type=Post.SONG_TYPE)

    def check_object_permissions(self, request, obj):
        pass

    @list_route()
    def popular(self, request):
        return self.do_pagination(queryset=Song.get_popular())

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Song.get_new())


class GenreViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    search_class = GenreSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        genres = Genre.objects.filter(parent__isnull=True)
        return self.do_pagination(queryset=genres)

    def get_queryset(self):
        return Genre.objects.all()

    @detail_route()
    def songs(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return self.do_pagination(queryset=genre.post_set.filter(subclass_type=Post.SONG_TYPE),
                                  serializer_class=PostSerializer)

    @detail_route()
    def karaokes(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return self.do_pagination(queryset=genre.post_set.filter(subclass_type=Post.KARAOKE_TYPE),
                                  serializer_class=PostSerializer)


class PoemViewSet(PermissionModelViewSet):
    serializer_class = PostSerializer
    search_class = PostSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Post.objects.filter(subclass_type=Post.POEM_TYPE)

    @detail_route()
    def full(self, request, pk):
        poem = Post.objects.get(id=pk)
        serialized = self.serializer_class(instance=poem, context={'request': self.request, 'detailed': True})
        return Response(serialized.data)

    @list_route()
    def popular(self, request):
        return self.do_pagination(queryset=Poem.get_popular())

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Poem.get_new())


class KaraokeViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = PostSerializer
    search_class = PostSearch

    def get_queryset(self):
        return Post.objects.filter(subclass_type=Post.KARAOKE_TYPE)
