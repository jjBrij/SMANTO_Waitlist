from django.urls import path
from .views import WaitlistCreateView, WaitlistCountView

urlpatterns = [
    path('api/join/', WaitlistCreateView.as_view(), name='waitlist-join'),
    path('api/count/', WaitlistCountView.as_view(), name='waitlist-count'),
]