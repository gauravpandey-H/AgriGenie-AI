from django.db import models

class WeatherAlert(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_issued = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
