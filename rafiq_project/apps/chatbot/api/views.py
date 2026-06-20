from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..services import get_rafiq_response
from ..models import Conversation, Message


@api_view(["POST"])
@permission_classes([AllowAny])
def chat(request):

    try:

        message = request.data.get("message")

        if not message:
            return Response(
                {"error": "message is required"},
                status=400
            )

        conversation_id = request.data.get(
            "conversation_id"
        )

        if not conversation_id:

            conversation = Conversation.objects.create()

        else:

            conversation = Conversation.objects.get(
                id=conversation_id
            )

        Message.objects.create(
            conversation=conversation,
            role="user",
            content=message
        )

        reply = get_rafiq_response(
            conversation.id
        )

        Message.objects.create(
            conversation=conversation,
            role="assistant",
            content=reply
        )

        return Response({
            "conversation_id": str(conversation.id),
            "reply": reply
        })

    except Exception as e:

        return Response({
            "error": str(e)
        }, status=500)