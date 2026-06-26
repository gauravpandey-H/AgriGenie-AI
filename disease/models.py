from django.db import models
from accounts.models import Farmer

class DiseasePrediction(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='disease_images/')
    disease_name = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    medicine = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    prevention = models.TextField(null=True, blank=True)
    predicted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disease_name} detected for {self.farmer.user.username}"
