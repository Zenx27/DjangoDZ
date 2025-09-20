from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Привет, {request.user.username}!"})

import jwt
from django.conf import settings
from django.http import JsonResponse

def manual_decode(request):
    token = request.headers.get("Authorization", "").split("Bearer ")[-1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS512"])
        return JsonResponse({"status": "ok", "user_id": payload.get("user_id")})
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=401)
