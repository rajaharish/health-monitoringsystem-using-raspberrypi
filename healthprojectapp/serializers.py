from healthprojectapp.models import health
from rest_framework import serializers

class HealthSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=health
		fields=('url','timestamp','name','temperature','pulse')
