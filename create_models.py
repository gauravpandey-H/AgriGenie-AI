import os

MODELS = {
    "accounts/models.py": """from django.db import models
from django.contrib.auth.models import User

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    preferred_language = models.CharField(max_length=50, default='English')

    def __str__(self):
        return f"{self.user.username}'s Profile"
""",
    "weather/models.py": """from django.db import models

class WeatherAlert(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_issued = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
""",
    "soil/models.py": """from django.db import models
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
""",
    "recommendation/models.py": """from django.db import models
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
""",
    "disease/models.py": """from django.db import models
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
""",
    "market/models.py": """from django.db import models

class MarketPrice(models.Model):
    crop_name = models.CharField(max_length=100)
    market_name = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_trend = models.CharField(max_length=50) # UP/DOWN
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} in {self.market_name} - {self.current_price}"
""",
    "notifications/models.py": """from django.db import models
from accounts.models import Farmer

class Notification(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
""",
    "government/models.py": """from django.db import models

class GovernmentScheme(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    eligibility = models.TextField()
    benefits = models.TextField()
    apply_link = models.URLField()
    required_documents = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
""",
    "chatbot/models.py": """from django.db import models
from accounts.models import Farmer

class ChatHistory(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.farmer.user.username} at {self.timestamp}"
"""
}

base_dir = r"c:\Users\gaurav\OneDrive\Desktop\sih-1"

for rel_path, content in MODELS.items():
    full_path = os.path.join(base_dir, rel_path)
    if os.path.exists(os.path.dirname(full_path)):
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Wrote {rel_path}")
    else:
        print(f"Warning: directory for {rel_path} not found.")
