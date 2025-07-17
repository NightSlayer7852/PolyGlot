from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import joblib
import os

class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        input_data = request.data.get("features")  # Expecting a list of features
        model_path = os.path.join(settings.BASE_DIR, "iris", "savedModels", "model.joblib")
        model = joblib.load(model_path)
        prediction = model.predict([input_data])
        predicted_class = ""
        if prediction[0]==0:
            predicted_class = "Setosa"
        elif prediction[0]==1:
            predicted_class = "Versicolor"
        else:
            predicted_class = "Virginica"
            
        return Response({"prediction": prediction[0],
                         "predicted_class": predicted_class})
