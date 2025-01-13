from rest_framework import serializers
from crmapp.models import Event, Category, Calendar

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'



class CalendarSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    events = serializers.SerializerMethodField()

    class Meta:
        model = Calendar
        fields = ['id', 'date', 'events']

    def get_events(self, obj):
        events_on_date = Event.objects.filter(
            start_time__date=obj.date
        ).order_by('start_time')
        return EventSerializer(events_on_date, many=True).data
