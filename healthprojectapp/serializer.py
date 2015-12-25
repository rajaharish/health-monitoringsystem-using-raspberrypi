from testapp.models import Mode,State
from rest_framework import serializers

class ModeSerializer(serializers.HyperLinkModelSerializer):
	class Meta:
		model=Mode
		fields=('url','name')

class StateSerializer(serializers.HyperLinkModeSerializer):
	class Meta:
		model=State
		fields('url','name')


