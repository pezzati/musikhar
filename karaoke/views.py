# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from karaoke.models import Post, Song, PostOwnerShip, Karaoke
from karaoke.serializers import GenrePostSerializer, PostSerializer
from mediafiles.models import MediaFile
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import Errors


class HomeFeed(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_new_posts(request):
        new_posts = Post.get_new(count=10, type=Post.KARAOKE_TYPE)
        serializer = PostSerializer(new_posts, many=True, context={'request': request})
        return dict(
            name=u'تازه‌ها',
            link='',
            files_link='https://{}{}'.format(request.domain, reverse('songs:get-post-news')),
            posts=serializer.data
        )

    @staticmethod
    def get_popular_posts(request):
        new_posts = Post.get_popular(count=10, type=Post.KARAOKE_TYPE)
        serializer = PostSerializer(new_posts, many=True, context={'request': request})
        return dict(
            name=u'محبوب‌ها',
            link='',
            files_link='https://{}{}'.format(request.domain, reverse('songs:get-post-popular')),
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


class CreateSong(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        file = request.FILES['file']
        data = request.POST

        name = data.get('name')
        desc = data.get('desc')
        tags = data.get('tags')
        karaoke_id = data.get('karaoke')

        if not karaoke_id:
            errors = Errors.get_errors(Errors, error_list=['Insufficient_Data'])
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            karaoke = Karaoke.objects.get(post_id=karaoke_id)
        except Karaoke.DoesNotExist:
            errors = Errors.get_errors(Errors, error_list=['Invalid_Info'])
            return Response(data=errors, status=status.HTTP_404_NOT_FOUND)

        if not name or name == '':
            name = karaoke.post.name

        post = Post.objects.create(
            name=name,
            description=desc,
            subclass_type=Post.SONG_TYPE,
            ownership_type=PostOwnerShip.USER_OWNER,
            is_premium=False,
            user=request.user
        )

        if tags:
            post.add_tags(tags.split(','))

        media_file = MediaFile.objects.create(user=request.user)
        media_file.file = file
        media_file.save()

        Song.objects.create(
            post=post,
            karaoke=karaoke,
            file=media_file
        )
        return Response(status=status.HTTP_201_CREATED)
