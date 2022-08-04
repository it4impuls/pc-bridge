from django.db import models

# Create your models here.
class Pc(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    mac = models.CharField(max_length=200)
    pcie_power = models.IntegerField(default=100)
    pcie_status = models.IntegerField(default=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name