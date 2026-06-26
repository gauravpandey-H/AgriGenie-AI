from django import forms
from .models import DiseasePrediction

class DiseaseUploadForm(forms.ModelForm):
    class Meta:
        model = DiseasePrediction
        fields = ['image']
        labels = {
            'image': 'Upload Leaf/Seed Image'
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                raise forms.ValidationError("Only image files (.jpg, .png, .jpeg, .webp) are accepted. Please upload a valid picture of a seed or plant.")
        return image
