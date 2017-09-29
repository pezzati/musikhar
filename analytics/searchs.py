from analytics.models import Tag
from musikhar.abstractions.search import ModelSearch


class TagSearch(ModelSearch):
    model = Tag
    search_fields = ('name',)
