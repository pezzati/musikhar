from django.db import models

from rest_framework import serializers
from rest_framework.fields import empty


class MySerializer(serializers.ModelSerializer):

    def run_validation(self, data=empty):
        if self.context.get('caller') and self.context.get('caller') != self.Meta.model:
            if data and data != empty:
                try:
                    model = self.Meta.model.objects.get(id=data.get('id'))
                    return model
                except models.ObjectDoesNotExist:
                    raise Exception(self.Meta.model)
            return None
        self.context['caller'] = self.Meta.model
        return super(MySerializer, self).run_validation(data=data)
