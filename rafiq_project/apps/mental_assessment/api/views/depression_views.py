from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..serializers.depression_serializers import DepressionTestSerializer
from ...utils.depression_utils import predict_depression
from ...models import DepressionTestResult

class DepressionTestApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DepressionTestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = serializer.validated_data
        result = predict_depression(validated_data)

        shared_url = None

        if request.user and request.user.is_authenticated:
            try:
                saved_result = DepressionTestResult.objects.create(
                    user=request.user,
                  depression=result.get("depression", "Unknown"),description=result.get("description", ""),
                    answers=validated_data
                )
                shared_url = f"https://rafiq-mentalhealth.com/share/depression/{saved_result.id}/"
            except Exception as database_error:
               print(f"Database save error: {database_error}")   

        response_data = {
            # "depression": result["depression"],
            "title": result["title"],
            "subtitle": result["subtitle"],
            "description": result["description"],
            "bottom_text": result["bottom_text"],
            "share_url": shared_url
        }
        return Response(response_data, status=200)
        
