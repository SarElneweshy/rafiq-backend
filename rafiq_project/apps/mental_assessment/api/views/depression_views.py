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

        response_data = {
            "depression": result["depression"],
            "description": result["description"],
            "suggestions": result["suggestions"],
            "video": result["video"],
        }
        if request.user.is_authenticated:
            DepressionTestResult.objects.create(
                user=request.user,
                depression=result["depression"],
                description=result["description"],
                suggestions=result["suggestions"],
                video_url=result["video"],
                answers=validated_data
            )

        return Response(response_data, status=200)
        
        # if request.user.is_authenticated:
        #     test = DepressionTestResult.objects.create(
        #         user=request.user,
        #         depression=result["depression"],
        #         description=result["description"],
        #         suggestions=result["suggestions"],
        #         video_url=result["video"],
        #         answers=validated_data
        #     )
        #     response_data["share_url"] = f"https://yourfrontend.com/result/{test.id}"
        # else:
        #     response_data["share_url"] = None

        # return Response(response_data, status=200)
