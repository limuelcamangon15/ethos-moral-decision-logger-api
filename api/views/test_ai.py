from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.services.groq_service import analyze_decision

@api_view(['GET'])
def test_ai(request):
    result = analyze_decision(
        context="I had a bad day and need to attend to a birthday party of my friend",
        action="I enjoyed the party and remain calm",
        reasoning="They must not be affected by my bad day",
        )
    return Response({'ai_result': result }, status=200)