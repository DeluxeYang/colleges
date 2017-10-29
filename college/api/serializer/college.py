from rest_framework import serializers

from basic.models import College


class CollegeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = College
        fields = ('url', 'id')
