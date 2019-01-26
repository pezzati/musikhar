import ast
import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from karaoke.models import Feed, Genre, Post
from karaoke.serializers import PostSerializer
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import conn, convert_to_dict

error_logger = logging.getLogger("error")


class HomeFeedV2(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        raw_data = conn().get('home_feed')
        if raw_data:
            print('YEAH')
            try:
                return Response(ast.literal_eval(raw_data.decode('utf-8')))
            except Exception as e:
                error_logger.info('[CACHE_RESPONSE_HOME_FFED] ERROR: {}, request: {}, raw_data: {}'.format(str(e),
                                                                                                 request.get_full_path(),
                                                                                                 raw_data))

        res = list()
        feeds = Feed.objects.all()
        feed_link_pattern = 'https://' + request.domain + '{}{}/karaokes'
        for feed in feeds:
            res.append(dict(
                name=feed.name,
                more=feed_link_pattern.format(reverse('songs:get-feed-list'), feed.code),
                data=PostSerializer(feed.get_query().order_by('?')[:10], many=True, context={'caller': Post, 'request': request}).data
                )
            )

        genres = Genre.objects.all()
        for genre in genres:
            res.append(
                dict(
                    name=genre.name,
                    more=feed_link_pattern.format(reverse('songs:get-genre-list'), genre.id),
                    data=PostSerializer(genre.post_set.all().order_by('?')[:10], many=True, context={'caller': Post, 'request': request}).data
                )
            )

        conn().set(name='home_feed', value=convert_to_dict(res), ex=86400)

        return Response(data=res)
