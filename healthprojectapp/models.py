from django.db import models

# Create your models here.

class health(models.Model):
	timestamp=models.DateTimeField(max_length=10)
	name=models.CharField(max_length=10)
	temperature=models.FloatField(max_length=4)
	pulse=models.FloatField(max_length=4)

