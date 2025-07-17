from django.db import models
from django.contrib.auth.models import User

class IrisPredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='iris_predictions', null=True, blank=True)
    sepal_length = models.FloatField()
    sepal_width = models.FloatField()
    petal_length = models.FloatField()
    petal_width = models.FloatField()
    predicted_class = models.CharField(max_length=50)
    input_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.predicted_class} at {self.input_time}"