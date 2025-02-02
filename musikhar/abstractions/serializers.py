from django.db import models

from rest_framework import serializers
from rest_framework.fields import empty


class MySerializer(serializers.ModelSerializer):
    identifier = 'id'
    key_identifier = 'id'
    create_on_validation = False

    def run_validation(self, data=empty):
        if self.context.get('caller') and self.context.get('caller') != self.Meta.model:
            if data and data != empty and data.get(self.key_identifier) and data.get(self.key_identifier) != 0:
                if self.create_on_validation:
                    model, created = self.Meta.model.objects.get_or_create(**{self.identifier: data.get(self.key_identifier)})
                    return model
                else:
                    try:
                        model = self.Meta.model.objects.get(**{self.identifier: data.get(self.key_identifier)})
                        return model
                    except models.ObjectDoesNotExist:
                        raise Exception('{} does not exists'.format(str(self.Meta.model)))
            return None
        self.context['caller'] = self.Meta.model
        return super(MySerializer, self).run_validation(data=data)

    def to_representation(self, instance):
        self.context['caller'] = self.Meta.model
        return super(MySerializer, self).to_representation(instance=instance)
