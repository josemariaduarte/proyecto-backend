from collections import OrderedDict
from django.db import models

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    list_display = []
    actividad_crear = None
    actividad_modificar = None
    table_columns = []



    def get_labels(self):
        ret = OrderedDict()
        fields = self._readable_fields
        for field in fields:
            if field.field_name != 'id':
                if not getattr(field, 'many', False):
                    ret[field.field_name] = field.label.title()
        return ret


    def get_table_columns(self):
        table_columns = []
        for field in self.table_columns:
            table_columns.append({"value": field, "text": self.get_fields()[field].label or field.capitalize()})
        return table_columns

