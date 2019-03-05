from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from karaoke.models import Post, PostOwnerShip, Karaoke, Song
from mediafiles.models import MediaFile
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import Errors


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

