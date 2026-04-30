from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from api.models import Analysis, Decision
from api.serializers import DecisionSerializer
from api.services.groq_service import analyze_decision, parse_ai_response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_decision(request):
    print("USER:", request.user)
    print("AUTH:", request.auth)
    serializer = DecisionSerializer(data=request.data)

    if serializer.is_valid():
        decision = serializer.save(user=request.user)

        ai_raw = analyze_decision(context=decision.context, action=decision.chosen_action, reasoning=decision.reasoning)

        parsed = parse_ai_response(ai_raw)

        if parsed:
            Analysis.objects.create(
                decision=decision,
                ethics=parsed.get("ethics", "unknown"),
                risk_level =parsed.get("risk_level", "unknown"),
                time_scope=parsed.get("time_scope", "unknown"),
                affected_party=parsed.get("affected_party", "unknown"),
                justification_quality=map_score(parsed.get("justification_quality")),
                confidence=map_score(parsed.get("confidence")),
                explanation=parsed.get("explanation", ""),
            )
        
        return Response({
            "decision": serializer.data,
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def map_score(value):
    mapping = {
        "low": 0.3,
        "medium": 0.6,
        "high": 0.9
    }
    return mapping.get(str(value).lower(), 0.0)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_decisions(request):
    decision = Decision.objects.filter(user=request.user).order_by('-created_at')

    serializers = DecisionSerializer(decision, many=True)

    return Response({
        "count": len(serializers.data),
        "results": serializers.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_insights(request):
    user = request.user

    decisions = Decision.objects.filter(user=user)

    total = decisions.count()

    ethics = (
        Analysis.objects
        .filter(decision__user=user)
        .values("ethics")
        .annotate(count=Count("ethics"))
    )

    risk = (
        Analysis.objects
        .filter(decision__user=user)
        .values("risk_level")
        .annotate(count=Count("risk_level"))
    )

    return Response({
        "total_decisions": total,
        "ethics_distribution": list(ethics),
        "risk_distribution": list(risk),
    }, status=status.HTTP_200_OK)