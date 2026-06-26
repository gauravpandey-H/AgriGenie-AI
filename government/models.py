from django.db import models

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
