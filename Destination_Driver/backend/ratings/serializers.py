from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'trip', 'client', 'score', 'comment']
        read_only_fields = ['id', 'trip', 'client']  # client & trip set by the view
