from django.db import models

class MarketPrice(models.Model):
    crop_name = models.CharField(max_length=100)
    market_name = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_trend = models.CharField(max_length=50) # UP/DOWN
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} in {self.market_name} - {self.current_price}"
