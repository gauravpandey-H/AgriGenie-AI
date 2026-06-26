from django.db import models
from accounts.models import Farmer

class SoilHealth(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    ph = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    moisture = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soil Health for {self.farmer.user.username} on {self.recorded_at.date()}"
