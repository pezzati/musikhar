from django_elasticsearch_dsl import DocType, Index, fields

from karaoke.models import Post

post = Index('posts')
post.settings(number_of_shards=1, number_of_replicas=0)


# genre = Index('genres')
# genre.settings(number_of_shards=1, number_of_replicas=0)


@post.doc_type
class PostDocument(DocType):
    # popularity = fields.IntegerField()
    # popularity_rate = fields.FloatField()
    # count =

    name = fields.TextField()
    tags = fields.ListField()

    class Meta:
        model = Post
        fields = [
            'popularity',
            'popularity_rate',
            'price',
            'count',
            # 'name',
            # 'tags',
            # 'genre',
            # 'description',
            'created_date'
        ]

