from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Components(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    def __str__(self):
        return str(self.user) + ' ' + str(self.name) + ' ' + str(self.x) + ' ' + str(self.y)

class Dashboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    def __str__(self):
        return str(self.user) + ' ' + str(self.height) + ' ' + str(self.width)
