from collections import defaultdict

from django.contrib.auth.models import User
from django.db.models import Count, F, Q
from django.db.models.functions import TruncDate, TruncMonth, TruncWeek, TruncYear
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import Blog, BlogView, Country
from analytics.serializers import (
    AnalyticsResponseSerializer,
    PerformanceAnalyticsResponseSerializer,
)
from utils.parse_filters import parse_dynamic_filters


class BlogViewsAnalyticsView(APIView):
    def get(self, request):
        object_type = request.query_params.get("object_type", "user")
        filters_json = request.query_params.get("filters", "{}")

        query_objects = parse_dynamic_filters(filters_json)
        queryset = Blog.objects.filter(query_objects)

        group_by = (
            "author__profile__country__name"
            if object_type == "country"
            else "author__username"
        )

        results = (
            queryset.values(group_by)
            .annotate(
                label=F(group_by),
                blog_count=Count("id", distinct=True),
                view_count=Count("views"),
            )
            .order_by("-view_count")
        )

        return Response(
            AnalyticsResponseSerializer(
                [
                    {
                        "x": res.get("label") or "Unknown",
                        "y": res.get("blog_count"),
                        "z": res.get("view_count"),
                    }
                    for res in results
                ],
                many=True,
            ).data
        )


class TopAnalyticsView(APIView):
    def get(self, request):
        top_type = request.query_params.get("top", "blog")
        filters_json = request.query_params.get("filters", "{}")
        query_objects = parse_dynamic_filters(filters_json)

        config = {
            "blog": {
                "queryset": Blog.objects.all(),
                "label": F("title"),
                "view_count": Count("views"),
                "secondary": F("author__username"),
            },
            "user": {
                "queryset": User.objects.all(),
                "label": F("username"),
                "view_count": Count("blogs__views"),
                "secondary": Count("blogs", distinct=True),
            },
            "country": {
                "queryset": Country.objects.all(),
                "label": F("name"),
                "view_count": Count("profiles__user__blogs__views"),
                "secondary": Count("profiles__user__blogs", distinct=True),
            },
        }

        if top_type not in config:
            return Response({"error": "Invalid top type"}, status=400)

        cfg = config[top_type]
        results = (
            cfg["queryset"]
            .filter(query_objects)
            .annotate(
                label=cfg["label"],
                view_count=cfg["view_count"],
                secondary=cfg["secondary"],
            )
            .values("label", "view_count", "secondary")
            .order_by("-view_count")[:10]
        )

        return Response(
            AnalyticsResponseSerializer(
                [
                    {
                        "x": res["label"],
                        "y": res["view_count"],
                        "z": res.get("secondary"),
                    }
                    for res in results
                ],
                many=True,
            ).data
        )


class PerformanceAnalyticsView(APIView):
    def get(self, request):
        compare = request.query_params.get("compare", "month")
        filters_json = request.query_params.get("filters", "{}")
        user_id = request.query_params.get("user_id", None)

        query_objects = parse_dynamic_filters(filters_json)
        if user_id:
            query_objects &= Q(author__id=user_id)

        trunc_func = {
            "day": TruncDate,
            "week": TruncWeek,
            "month": TruncMonth,
            "year": TruncYear,
        }.get(compare, TruncMonth)

        blog_queryset = Blog.objects.filter(query_objects)
        blog_stats = (
            blog_queryset.annotate(period=trunc_func("created_at"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )

        view_queryset = BlogView.objects.filter(blog__in=blog_queryset)
        view_stats = (
            view_queryset.annotate(period=trunc_func("timestamp"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )

        merged_stats = defaultdict(lambda: {"blogs": 0, "views": 0})
        for blog in blog_stats:
            if blog["period"]:
                merged_stats[blog["period"]]["blogs"] = blog["count"]

        for view in view_stats:
            if view["period"]:
                merged_stats[view["period"]]["views"] = view["count"]

        sorted_periods = sorted(merged_stats.keys())
        response_data = []
        prev_views = 0
        for period in sorted_periods:
            values = merged_stats[period]
            views = values["views"]
            blogs = values["blogs"]
            label = period.strftime("%Y-%m-%d")

            growth = "0%"
            if prev_views > 0:
                change = ((views - prev_views) / prev_views) * 100
                growth = "{}{:.2f}%".format("+" if change > 0 else "", change)

            response_data.append(
                {"x": f"{label} ({blogs} blogs)", "y": views, "z": growth}
            )
            prev_views = views

        return Response(
            PerformanceAnalyticsResponseSerializer(response_data, many=True).data
        )
