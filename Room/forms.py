from Room.models import Review
from django import forms


class AddReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',
                  'rating',)
