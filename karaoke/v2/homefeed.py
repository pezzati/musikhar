from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from karaoke.models import Feed, Genre, Post
from karaoke.serializers import PostSerializer
from musikhar.abstractions.views import IgnoreCsrfAPIView


class HomeFeedV2(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        res = list()
        feeds = Feed.objects.all()
        feed_link_pattern = 'http://' + request.domain + '{}{}/karaokes'
        for feed in feeds:
            res.append(dict(
                name=feed.name,
                more=feed_link_pattern.format(reverse('songs:get-feed-list'), feed.code),
                data=PostSerializer(feed.get_query()[:10], many=True, context={'caller': Post, 'request': request}).data
                )
            )

        genres = Genre.objects.all()
        for genre in genres:
            res.append(
                dict(
                    name=genre.name,
                    more=feed_link_pattern.format(reverse('songs:get-genre-list'), genre.id),
                    data=PostSerializer(genre.post_set.all()[:10], many=True, context={'caller': Post, 'request': request}).data
                )
            )
        return Response(data=res)
