from rest_framework import serializers
from .models import Machine, TO, Complaint


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ('__all__')

class TOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TO
        fields = ('__all__')

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('__all__')
