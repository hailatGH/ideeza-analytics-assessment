from django.urls import path

from analytics.views import (
    BlogViewsAnalyticsView,
    PerformanceAnalyticsView,
    TopAnalyticsView,
)

urlpatterns = [
    path("blog-views/", BlogViewsAnalyticsView.as_view(), name="blog-views"),
    path("top/", TopAnalyticsView.as_view(), name="top-analytics"),
    path(
        "performance/", PerformanceAnalyticsView.as_view(), name="performance-analytics"
    ),
]
