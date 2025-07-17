from rest_framework import serializers
from .models import IrisPredictionHistory

class IrisPredictionSerializer(serializers.Serializer):
    sepal_length = serializers.FloatField(required=True, help_text="Sepal length in cm")
    sepal_width = serializers.FloatField(required=True, help_text="Sepal width in cm")
    petal_length = serializers.FloatField(required=True, help_text="Petal length in cm")
    petal_width = serializers.FloatField(required=True, help_text="Petal width in cm")

    def validate(self, data):
        # Ensure only the four required fields are provided
        allowed_fields = {'sepal_length', 'sepal_width', 'petal_length', 'petal_width'}
        if set(data.keys()) != allowed_fields:
            raise serializers.ValidationError(
                f"Only the following fields are allowed: {', '.join(allowed_fields)}"
            )
        # Validate that values are non-negative
        for field in allowed_fields:
            if data[field] < 0:
                raise serializers.ValidationError(f"{field} must be a non-negative number")
        return data

class IrisPredictionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IrisPredictionHistory
        fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'predicted_class', 'input_time']