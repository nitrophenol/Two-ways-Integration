from django.db import models

# Create your models here.
from django.db import models

class Customer(models.Model):
    id = models.AutoField()  # Your specific ID field
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,primary_key=True)

    def __str__(self):
        return self.name
