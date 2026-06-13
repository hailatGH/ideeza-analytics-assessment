from rest_framework import serializers


class AnalyticsResponseSerializer(serializers.Serializer):
    x = serializers.CharField()
    y = serializers.IntegerField()
    z = serializers.ReadOnlyField()  # can handle string, int, or float dynamically


class PerformanceAnalyticsResponseSerializer(serializers.Serializer):
    x = serializers.CharField()
    y = serializers.FloatField()
    z = serializers.CharField()  # saves percentage as string with +/-
