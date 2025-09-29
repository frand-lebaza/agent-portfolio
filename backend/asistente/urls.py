from django.urls import path
from .views import AgentViewset

urlpatterns = [   
    # API endpoints for the virtual assistant surgeon    
    path('responder-ia/', AgentViewset.as_view({'post': 'responder'}), name='responder_ia'),        
]

