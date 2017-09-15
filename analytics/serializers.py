from analytics.models import Tag
from musikhar.abstractions.serializers import MySerializer


class TagSerializer(MySerializer):
    identifier = 'name'
    create_on_validation = True

    class Meta:
        model = Tag
        fields = ('name',)
