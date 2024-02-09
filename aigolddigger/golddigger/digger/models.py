from django.db import models

# Create your models here.
class CryptoTable  (models.Model):
    pair = models.CharField(max_length=30, default="BTCUSDT")
    time=  models.DateTimeField()
    open_time=  models.DateTimeField()
    close_time=  models.DateTimeField()
    open= models.DecimalField(decimal_places=50, max_digits=200)
    high= models.DecimalField(decimal_places=50, max_digits=200)
    low= models.DecimalField(decimal_places=50, max_digits=200)
    close= models.DecimalField(decimal_places=50, max_digits=200)
    
 
