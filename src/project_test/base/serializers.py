from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'created_by', 'modified_by', 'title', 'start', 'end', 'color', 'allDay' , 'created', 'modified']
        read_only_fields = ['created_by', 'modified_by' 'created', 'modified']  # No permite modificar estos campos
