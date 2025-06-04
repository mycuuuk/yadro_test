from django.urls import path
from .views import (
    RedirectView,
    LinkCreateView,
    LinkListView,
    LinkDeactivateView,
    LinkStatisticsView
)
urlpatterns = [
    path('links/', LinkListView.as_view(), name='link-list'),
    path('links/create/', LinkCreateView.as_view(), name='link-create'),
    path('links/<int:pk>/deactivate/', LinkDeactivateView.as_view(), name='link-deactivate'),
    path('statistics/', LinkStatisticsView.as_view(), name='link-stats'),
    path('<str:short_code>/', RedirectView.as_view(), name='redirect'),
]