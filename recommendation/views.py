from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CropRecommendationForm
from .services import CropRecommendationService
from .models import CropRecommendation

@login_required
def predict_crop_view(request):
    if request.method == 'POST':
        form = CropRecommendationForm(request.POST)
        if form.is_valid():
            # Get the features
            features = form.cleaned_data
            
            # Predict
            service = CropRecommendationService()
            prediction = service.predict_crop({
                'N': features['nitrogen'],
                'P': features['phosphorus'],
                'K': features['potassium'],
                'temperature': features['temperature'],
                'humidity': features['humidity'],
                'ph': features['ph'],
                'rainfall': features['rainfall'],
            })
            
            # Save to DB
            record = CropRecommendation.objects.create(
                farmer=request.user.farmer,
                temperature=features['temperature'],
                humidity=features['humidity'],
                rainfall=features['rainfall'],
                ph=features['ph'],
                nitrogen=features['nitrogen'],
                phosphorus=features['phosphorus'],
                potassium=features['potassium'],
                season=features['season'],
                location=features['location'],
                recommended_crop=prediction['crop'],
                confidence=prediction['confidence'],
                expected_yield=prediction.get('expected_yield_per_hectare'),
                estimated_profit=prediction.get('estimated_profit')
            )
            
            # Show result
            return render(request, 'recommendation/predict_result.html', {'record': record, 'prediction': prediction})
    else:
        form = CropRecommendationForm()
    
    return render(request, 'recommendation/predict_form.html', {'form': form})

