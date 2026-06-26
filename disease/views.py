from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DiseaseUploadForm
from .models import DiseasePrediction
import hashlib
import random

DISEASES = [
    {
        "name": "Leaf Rust",
        "confidence": 0.89,
        "medicine": "Apply fungicide containing Tebuconazole",
        "treatment": "Remove infected leaves and burn them.",
        "prevention": "Ensure proper spacing between crops to allow air circulation."
    },
    {
        "name": "Powdery Mildew",
        "confidence": 0.94,
        "medicine": "Sulfur-based fungicides or Neem oil",
        "treatment": "Prune affected areas immediately.",
        "prevention": "Avoid overhead watering and keep foliage dry."
    },
    {
        "name": "Blight",
        "confidence": 0.82,
        "medicine": "Copper-based fungicides",
        "treatment": "Destroy infected plant debris.",
        "prevention": "Use certified disease-free seeds and practice crop rotation."
    },
    {
        "name": "Healthy Plant",
        "confidence": 0.98,
        "medicine": "None required",
        "treatment": "Continue regular maintenance.",
        "prevention": "Maintain optimal watering and fertilizer schedules."
    }
]

@login_required
def disease_detect_view(request):
    if request.method == 'POST':
        form = DiseaseUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES.get('image')
            
            # 1. Mock Validation: Check if it's a seed or tree/plant
            # In production, this would be a classification model.
            # Here we mock it by checking if the filename contains invalid words.
            invalid_keywords = ['dog', 'cat', 'person', 'car', 'house', 'animal', 'selfie', 'food']
            filename = image_file.name.lower()
            if any(word in filename for word in invalid_keywords):
                messages.error(request, "Wrong file")
                return redirect('disease_detect')
            
            # 2. Deterministic Prediction: Same image returns same details
            # Calculate MD5 hash of the image content
            file_content = image_file.read()
            image_hash = hashlib.md5(file_content).hexdigest()
            image_file.seek(0) # Reset file pointer after reading
            
            # Seed the random generator with the image hash
            random.seed(image_hash)
            
            # Pick a deterministic disease based on the seed
            result = random.choice(DISEASES)
            
            # Save Prediction
            prediction = form.save(commit=False)
            prediction.farmer = request.user.farmer
            prediction.disease_name = result["name"]
            
            # Add some deterministic noise to the confidence score (between -0.05 and +0.05)
            noise = random.uniform(-0.05, 0.05)
            prediction.confidence_score = min(0.99, max(0.50, result["confidence"] + noise))
            
            prediction.medicine = result["medicine"]
            prediction.treatment = result["treatment"]
            prediction.prevention = result["prevention"]
            
            prediction.save()
            
            # Reset random seed back to system time for other processes
            random.seed()
            
            return render(request, 'disease/detect_result.html', {'prediction': prediction})
    else:
        form = DiseaseUploadForm()
    
    return render(request, 'disease/upload_form.html', {'form': form})

