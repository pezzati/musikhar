# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from karaoke.models import Post
from karaoke.serializers import GenrePostSerializer, PostSerializer
from musikhar.abstractions.views import IgnoreCsrfAPIView


class HomeFeed(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_new_posts(request):
        new_posts = Post.get_new(count=10, type=Post.KARAOKE_TYPE)
        serializer = PostSerializer(new_posts, many=True, context={'request': request})
        return dict(
            name=u'تازه‌ها',
            link='',
            files_link='http://{}{}'.format(request.domain, reverse('songs:get-post-news')),
            posts=serializer.data
        )

    @staticmethod
    def get_popular_posts(request):
        new_posts = Post.get_popular(count=10, type=Post.KARAOKE_TYPE)
        serializer = PostSerializer(new_posts, many=True, context={'request': request})
        return dict(
            name=u'محبوب‌ها',
            link='',
            files_link='http://{}{}'.format(request.domain, reverse('songs:get-post-popular')),
            posts=serializer.data
        )

    def get(self, request):
        user = request.user
        genres = user.genres
        serializer = GenrePostSerializer(genres, many=True, context={'request': request})
        res = serializer.data
        res.append(self.get_new_posts(request=request))
        res.append(self.get_popular_posts(request=request))
        return Response(data=res)
