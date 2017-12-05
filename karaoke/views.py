from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from karaoke.models import Post
from karaoke.serializers import GenrePostSerializer, PostSerializer
from musikhar.abstractions.views import IgnoreCsrfAPIView


class HomeFeed(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def get_new_posts(self, request):
        new_posts = Post.get_new(count=10)
        serializer = PostSerializer(new_posts, many=True)
        return dict(
            name='News',
            link='',
            files_link='',
            posts=serializer.data
        )

    def get_popular_posts(self, request):
        new_posts = Post.get_popular(count=10)
        serializer = PostSerializer(new_posts, many=True)
        return dict(
            name='Popular',
            link='',
            files_link='',
            posts=serializer.data
        )

    def get(self, request):
        user = request.user
        genres = user.genres
        serializer = GenrePostSerializer(genres, many=True)
        res = serializer.data
        res.append(self.get_new_posts(request=request))
        res.append(self.get_popular_posts(request=request))
        return Response(data=res)
