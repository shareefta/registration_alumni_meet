from django.db import models

# Create your models here.
class Alumni(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    whatsapp_number = models.CharField(max_length=15)
    name_of_wife = models.CharField(max_length=15, blank=True, default=None)
    no_of_child_below_5 = models.IntegerField(default=0)
    no_of_child_above_5 = models.IntegerField(default=0)
    is_registered = models.BooleanField(default=False)
    
    # def __str__(self) -> str:
    #     return self.name
    
    class Meta:
        ordering = ['name']
    