from django.db import models
from accounts.models import Farmer

class CropRecommendation(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    ph = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    season = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    
    recommended_crop = models.CharField(max_length=100)
    confidence = models.FloatField()
    expected_yield = models.FloatField(null=True, blank=True)
    estimated_profit = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recommended_crop} for {self.farmer.user.username}"

class CropHistory(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    date_planted = models.DateField()
    date_harvested = models.DateField(null=True, blank=True)
    yield_amount = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.crop_name} - {self.farmer.user.username}"
