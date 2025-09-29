from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from asistente.agents.agent_config import responder_ia_langchain

import json, os, requests, pytz
from django.http.response import JsonResponse
from django.conf import settings
from datetime import datetime
import random
from openai import OpenAIError
from asistente.agents.session_manager import get_session, set_session, clear_session


class AgentViewset(viewsets.GenericViewSet):
    @action(detail=False, methods=['post'])
    def responder(self, request):
        mensaje = request.data.get('mensaje')
        thread_id = request.data.get('thread_id')
        # session_id = request.data.get('session_id')

        if not mensaje:
            return JsonResponse({'error': 'Falta el mensaje.'}, status=400)

        if not thread_id:
            return JsonResponse({'error': 'Falta el id de user.'}, status=400)

        try:
            respuesta = responder_ia_langchain(mensaje, thread_id)
            return JsonResponse({'respuesta': respuesta}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        