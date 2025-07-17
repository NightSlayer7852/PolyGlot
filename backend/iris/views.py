from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated  # Change to AllowAny for public access
from rest_framework.response import Response
from rest_framework import status
import joblib
import os
from .serializers import IrisPredictionSerializer, IrisPredictionHistorySerializer
from .models import IrisPredictionHistory

class IrisPredictView(APIView):
    permission_classes = [AllowAny]  # Set to [AllowAny] if public access is desired

    def post(self, request):
        # Validate input data
        serializer = IrisPredictionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        data = serializer.validated_data
        input_data = [
            data['sepal_length'],
            data['sepal_width'],
            data['petal_length'],
            data['petal_width']
        ]

        # Load model
        model_path = os.path.join(settings.BASE_DIR, "iris", "savedModels", "model.joblib")
        if not os.path.exists(model_path):
            return Response({"error": "Model file not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            model = joblib.load(model_path)
            prediction = model.predict([input_data])[0]
            predicted_class = {
                0: "Setosa",
                1: "Versicolor",
                2: "Virginica"
            }.get(prediction, "Unknown")
        except Exception as e:
            return Response({"error": f"Prediction failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save to history
        history = IrisPredictionHistory(
            user=request.user if self.permission_classes == [IsAuthenticated] else None,
            sepal_length=data['sepal_length'],
            sepal_width=data['sepal_width'],
            petal_length=data['petal_length'],
            petal_width=data['petal_width'],
            predicted_class=predicted_class
        )
        history.save()

        # Serialize history for response
        history_serializer = IrisPredictionHistorySerializer(history)
        return Response({
            "prediction": prediction,
            "predicted_class": predicted_class,
            "history": history_serializer.data
        }, status=status.HTTP_200_OK)