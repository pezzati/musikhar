# -*- coding: utf-8 -*-
import json
import ast

from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
# from silk.profiling.profiler import silk_profile

from analytics.models import UserFileHistory, Like, Favorite
from karaoke.searchs import PostSearch, GenreSearch, KaraokeSearch
from karaoke.serializers import GenreSerializer, PostSerializer, SingleGenreSerializer, FeedSerializer
from karaoke.models import Genre, Post, Feed
from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.serializers import UserInfoSerializer
from musikhar.abstractions.exceptions import NoFileInPost
from musikhar.abstractions.views import PermissionModelViewSet, PermissionReadOnlyModelViewSet
# from musikhar.middlewares import error_logger
from musikhar.utils import conn, convert_to_dict, Errors


class PostViewSet(PermissionModelViewSet):
    serializer_class = PostSerializer
    search_class = PostSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Post.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.context['full_data'] = True
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(subclass_type=Post.KARAOKE_TYPE)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def check_object_permissions(self, request, obj):
        if obj.user_has_access(request.user):
            pass
        else:
            raise NotAuthenticated

    @detail_route(methods=['get'], permission_classes=())
    def file(self, request, pk):
        try:
            target_post = Post.objects.get(id=pk)
            target_file = target_post.get_file(request.GET.get('target'))
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
            post.rate += 1
            post.save()
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'GET':
            return self.do_pagination(queryset=post.likes.all(), serializer_class=UserInfoSerializer)
        elif request.method == 'DELETE':
            try:
                Like.objects.get(user=request.user, post=post).delete()
                post.rate -= 1
                post.save()
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

    @list_route()
    def popular(self, request):
        cached_response = self.cache_response(request=request)
        if cached_response:
            return cached_response

        return self.do_pagination(queryset=Post.get_popular(type=Post.KARAOKE_TYPE, count=20),
                                  cache_key=request.get_full_path(),
                                  cache_time=86400)

    @list_route()
    def news(self, request):
        cached_response = self.cache_response(request=request)
        if cached_response:
            return cached_response

        return self.do_pagination(queryset=Post.get_new(type=Post.KARAOKE_TYPE),
                                  cache_key=request.get_full_path(),
                                  cache_time=604800)

    @list_route()
    def free(self, request):
        cached_response = self.cache_response(request=request)
        if cached_response:
            return cached_response

        return self.do_pagination(queryset=Post.get_free(type=Post.KARAOKE_TYPE),
                                  cache_key=request.get_full_path(),
                                  cache_time=86400)

    @list_route()
    def feeds(self, request):
        data = conn().get('feeds')
        if data is None:
            base_url = 'http://{}{}'.format(request.domain, reverse('songs:get-genre-list'))
            data = [
                dict(name=u'داغ', url=base_url + 'news')
            ]
            conn().set(name='feeds', value=data, ex=3600)
        else:
            data = ast.literal_eval(data.decode('utf-8'))
        return Response(data=data)


class SongViewSet(PermissionModelViewSet):
    serializer_class = PostSerializer
    search_class = PostSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    # @silk_profile(name='View Songs')
    def get_queryset(self):
        return Post.objects.filter(subclass_type=Post.SONG_TYPE)

    def check_object_permissions(self, request, obj):
        pass

    @list_route()
    def popular(self, request):
        return self.do_pagination(queryset=Post.get_popular(type=Post.SONG_TYPE))

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Post.get_new(type=Post.SONG_TYPE))

    @list_route()
    def free(self, request):
        return self.do_pagination(queryset=Post.get_free(type=Post.SONG_TYPE))


# from rest_framework.pagination import PageNumberPagination
class GenreViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    search_class = GenreSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Genre.objects.all()

    @detail_route()
    def songs(self, request, pk):
        cached_response = self.cache_response(request=request)
        if cached_response:
            return cached_response

        try:
            genre = Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return self.do_pagination(queryset=genre.post_set.filter(subclass_type=Post.SONG_TYPE),
                                  serializer_class=PostSerializer,
                                  cache_key=request.get_full_path(),
                                  cache_time=3600)

    @detail_route()
    def karaokes(self, request, pk):
        cached_response = self.cache_response(request=request)
        if cached_response:
            return cached_response

        try:
            genre = Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return self.do_pagination(queryset=genre.post_set.filter(subclass_type=Post.KARAOKE_TYPE),
                                  serializer_class=PostSerializer,
                                  cache_key=request.get_full_path(),
                                  cache_time=3600)

    @list_route(methods=['post', 'get'])
    def favorite(self, request):
        user = request.user
        if request.method == 'GET':
            return self.do_pagination(queryset=user.genres.all(), serializer_class=SingleGenreSerializer)

        genres = json.loads(request.body.decode('utf-8'))
        if request.method == 'POST':
            user.genres = Genre.objects.none()
            for genre_name in genres:
                try:
                    user.genres.add(Genre.objects.get(name=genre_name))
                except Genre.DoesNotExist:
                    pass
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @list_route(methods=['post'])
    def unfavorite(self, request):
        user = request.user
        genres = json.loads(request.body.decode('utf-8'))
        for genre_name in genres:
            try:
                user.genres.remove(Genre.objects.get(name=genre_name))
            except Genre.DoesNotExist:
                pass
        return Response(status=status.HTTP_202_ACCEPTED)


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
        return self.do_pagination(queryset=Post.get_popular(type=Post.POEM_TYPE))

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Post.get_new(type=Post.POEM_TYPE))

    @list_route()
    def free(self, request):
        return self.do_pagination(queryset=Post.get_free(type=Post.POEM_TYPE))


class KaraokeViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = PostSerializer
    search_class = KaraokeSearch

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Post.objects.filter(subclass_type=Post.KARAOKE_TYPE)

    @list_route()
    def popular(self, request):
        return self.do_pagination(queryset=Post.get_popular(type=Post.KARAOKE_TYPE))

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Post.get_new(type=Post.KARAOKE_TYPE))

    @list_route()
    def free(self, request):
        return self.do_pagination(queryset=Post.get_free(type=Post.KARAOKE_TYPE))


class FeedViewSet(PermissionReadOnlyModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    lookup_field = 'code'
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @detail_route()
    def karaokes(self, request, code):
        cached_response = self.cache_response(request=request)
        if cached_response:
            print('HIT')
            return cached_response

        try:
            feed = Feed.objects.get(code=code)
        except Feed.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return self.do_pagination(queryset=feed.get_query(),
                                  serializer_class=PostSerializer,
                                  cache_key=request.get_full_path(),
                                  cache_time=1800)
