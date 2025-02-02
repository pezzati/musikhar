from django.db import models
from django.db.models import Q


class ModelSearch(object):
    model = models.Model
    search_fields = ('name',)
    search_type = '__icontains'
    model_has_tags = False
    tags_key = 'tags'
    __query = Q()

    def __create_query(self, search_key, tags=[]):
        if not search_key and not tags:
            self.__query = None
            return

        self.__query = Q()
        if search_key:
            for field in self.search_fields:
                self.__query = self.__query | Q(**{'{}{}'.format(field, self.search_type): search_key})

        if self.model_has_tags and tags:
            query_tags = Q()
            for tag in tags:
                if tag[0] != '#':
                    tag = '#{}'.format(tag)
                query_tags = query_tags | Q(**{'{}__name__iexact'.format(self.tags_key): tag})

            self.__query = self.__query & query_tags

    def get_result(self, search_key, tags=[], query_set=None):
        self.__create_query(search_key=search_key, tags=tags)
        if not query_set:
            query_set = self.model.objects
        if self.__query:
            return query_set.filter(self.__query)
        else:
            return self.model.objects.none()
