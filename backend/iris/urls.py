from django.urls import path
from .views import IrisPredictView

urlpatterns = [
    path('predict/', IrisPredictView.as_view(), name='iris_predict'),
]