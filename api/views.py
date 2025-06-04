from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.utils import timezone
from .models import Link, ClickLog
from .serializers import LinkSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(auto_schema=None)
class RedirectView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, short_code):
        link = get_object_or_404(Link, short_code=short_code)

        if not link.is_active or link.is_expired():
            return Response({"detail": "Link is inactive or expired."}, status=status.HTTP_410_GONE)

        link.click_count += 1
        link.save()

        ClickLog.objects.create(link=link)

        return redirect(link.original_url)


class LinkCreateView(generics.CreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            expires_at=timezone.now() + timedelta(days=1)
        )

class LinkListView(generics.ListAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['original_url']
    ordering_fields = ['created_at', 'click_count']

    def get_queryset(self):
        queryset = Link.objects.filter(created_by=self.request.user)
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset

class LinkDeactivateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        link = get_object_or_404(Link, pk=pk, created_by=request.user)
        link.is_active = False
        link.save()
        return Response({"detail": "Link deactivated."}, status=200)

class LinkStatisticsView(generics.ListAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'sort_by',
            openapi.IN_QUERY,
            description="Тип сортировки:\n"
                        "`total` — по общему количеству\n"
                        "`hour` — по кликам за последний час\n"
                        "`day` — по кликам за последние сутки",
            type=openapi.TYPE_STRING,
            enum=['total', 'hour', 'day']
        )
    ])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        sort_by = self.request.query_params.get('sort_by', 'total')
        user_links = Link.objects.filter(created_by=self.request.user)

        if sort_by == 'hour':
            one_hour_ago = timezone.now() - timedelta(hours=1)
            return sorted(
                user_links,
                key=lambda link: link.click_logs.filter(timestamp__gte=one_hour_ago).count(),
                reverse=True
            )

        elif sort_by == 'day':
            one_day_ago = timezone.now() - timedelta(days=1)
            return sorted(
                user_links,
                key=lambda link: link.click_logs.filter(timestamp__gte=one_day_ago).count(),
                reverse=True
            )

        return user_links.order_by('-click_count')


