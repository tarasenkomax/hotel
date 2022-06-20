from Room.models import Review
from django import forms


class ReviewForm(forms.ModelForm):
    """ Форма добавления отзыва """
    class Meta:
        model = Review
        fields = ('body',
                  'rating',)

    def clean_body(self):
        body = self.cleaned_data['body']
        if len(body) > 500:
            raise forms.ValidationError("Отзыв не должен превышать 500 символов")
        return body

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if 0 > rating or rating > 5:
            raise forms.ValidationError("Рейтинг должен быть в диапазоне от 1 до 5")
        return rating
