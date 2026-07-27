from rest_framework import generics, status
from rest_framework.response import Response
from .models import WaitlistEntry
from .serializers import WaitlistEntrySerializer
from django.core.mail import send_mail
from django.conf import settings
import traceback

class WaitlistCreateView(generics.CreateAPIView):
    queryset = WaitlistEntry.objects.all()
    serializer_class = WaitlistEntrySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Get real position (count of all entries)
        position = WaitlistEntry.objects.count()
        
        # Send auto-reply email (non-blocking)
        email = serializer.validated_data.get('email')
        comment = serializer.validated_data.get('comment', '')
        if email:
            self.send_auto_reply(email, comment)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            "success": True,
            "position": position,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def send_auto_reply(self, email, comment):
        try:
            send_mail(
                subject="Welcome to Smanto Waitlist!",
                message=f"Hi there,\n\nThank you for joining the Smanto waitlist!\n\nYour comment: {comment}\n\nWe'll reach out soon.\n\n- Smanto Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            print(f"✅ Email sent to {email}")
        except Exception as e:
            print(f"❌ Email failed: {e}")
            traceback.print_exc()

class WaitlistCountView(generics.GenericAPIView):
    def get(self, request):
        count = WaitlistEntry.objects.count()
        return Response({"count": count})