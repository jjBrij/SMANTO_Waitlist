from rest_framework import serializers
from .models import WaitlistEntry

class WaitlistEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitlistEntry
        fields = ['id', 'email', 'phone', 'comment', 'created_at']

    def validate(self, data):
        email = data.get('email')
        phone = data.get('phone')
        
        if not email and not phone:
            raise serializers.ValidationError("Either email or phone number is required.")
        
        # Check for duplicates
        if email and WaitlistEntry.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already on the waitlist.")
        if phone and WaitlistEntry.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("This phone number is already on the waitlist.")
            
        return data