from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from analytics.models import UserFileHistory
from karaoke.searchs import PostSearch, GenreSearch
from karaoke.serializers import SongSerializer, GenreSerializer, PoemSerializer, PostSerializer
from karaoke.models import Song, Genre, Poem, Post
from loginapp.auth import CsrfExemptSessionAuthentication
from mediafiles.models import MediaFile
from musikhar.abstractions.exceptions import NoFileInPost
from musikhar.abstractions.views import PermissionModelViewSet, PermissionReadOnlyModelViewSet
from musikhar.utils import Errors


class PostViewSet(PermissionReadOnlyModelViewSet):
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


class SongViewSet(PermissionModelViewSet):
    serializer_class = SongSerializer
    search_class = PostSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @silk_profile(name='View Songs')
    def get_queryset(self):
        user = self.request.user
        return Song.objects.all()

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
        genre = Genre.objects.get(pk=pk)
        return self.do_pagination(queryset=genre.song_set.all(), serializer_class=SongSerializer)


class PoemViewSet(PermissionModelViewSet):
    serializer_class = PoemSerializer
    search_class = PostSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Poem.objects.all()

    @detail_route()
    def full(self, request, pk):
        poem = Poem.objects.get(id=pk)
        serialized = self.serializer_class(instance=poem, context={'request': self.request, 'detailed': True})
        return Response(serialized.data)

    @list_route()
    def popular(self, request):
        return self.do_pagination(queryset=Poem.get_popular())

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Poem.get_new())

