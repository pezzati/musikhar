from django.db import models
from django.db.models import Q


class ModelSearch(object):
    model = models.Model
    search_fields = ('name',)
    search_type = '__contains'
    __query = Q()

    def __create_query(self, search_key):
        self.__query = Q()
        if not search_key:
            raise Exception('search key can not be none')
        if not isinstance(search_key, str):
            raise Exception('search key must be string')
        for field in self.search_fields:
            self.__query = self.__query | Q(**{'{}{}'.format(field, self.search_type): search_key})

    def get_result(self, search_key):
        self.__create_query(search_key=search_key)
        return self.model.objects.filter(self.__query)
