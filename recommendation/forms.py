from django import forms

class CropRecommendationForm(forms.Form):
    temperature = forms.FloatField(label="Temperature (°C)")
    humidity = forms.FloatField(label="Humidity (%)")
    rainfall = forms.FloatField(label="Rainfall (mm)")
    ph = forms.FloatField(label="Soil pH")
    nitrogen = forms.FloatField(label="Nitrogen (N)")
    phosphorus = forms.FloatField(label="Phosphorus (P)")
    potassium = forms.FloatField(label="Potassium (K)")
    season = forms.CharField(label="Season", max_length=50)
    location = forms.CharField(label="Location/District", max_length=100)
