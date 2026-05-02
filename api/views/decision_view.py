from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.utils import timezone
from datetime import timedelta

from api.models import Analysis, Decision
from api.serializers import DecisionSerializer
from api.services.groq_service import analyze_decision, parse_ai_response

# post a decision a logged-in user made
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

# get one decision of logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_decision(request, pk):
    user = request.user

    decision = Decision.objects.filter(id=pk, user=user).first()

    if decision is None:
        return Response({"message": "Decision not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DecisionSerializer(decision)

    return Response(serializer.data, status=status.HTTP_200_OK)


# get all decisions of logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_decisions(request):
    decision = Decision.objects.filter(user=request.user).order_by('-created_at')

    serializers = DecisionSerializer(decision, many=True)

    return Response({
        "count": len(serializers.data),
        "results": serializers.data
    }, status=status.HTTP_200_OK)


# --------------------- Dashboard ------------------------

# get user insights for dashboard
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


# get all decisions count everyweek
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weekly_decisions_count(request):
    today = timezone.now()
    seven_days_ago = today - timedelta(days=7)

    qs = Decision.objects.filter(created_at__gte=seven_days_ago)

    qs = qs.annotate(
            weekday=ExtractWeekDay('created_at')
        ).values('weekday').annotate(count=Count('id'))

    weekday_map = {
        1: 'sunday',
        2: 'monday',
        3: 'tuesday',
        4: 'wednesday',
        5: 'thursday',
        6: 'friday',
        7: 'saturday',
    }

    result = {day: 0 for day in weekday_map.values()}

    for item in qs:
        day_name = weekday_map[item['weekday']]
        result[day_name] = item['count']
    
    return Response(result, status=status.HTTP_200_OK)