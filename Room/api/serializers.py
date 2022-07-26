from rest_framework import serializers

from Room.models import Room, Gallery, Regulations, Review, Reserve


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['slider_photo1', 'slider_photo2', 'slider_photo3', 'slider_photo4']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'body', 'author', 'reserve', 'pub_date']


class RegulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regulations
        fields = ['id', 'regulation']


class RoomDetailSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(source="photos_of_room")
    regulations = RegulationSerializer(many=True, source="get_regulations_list")
    reviews = ReviewSerializer(many=True, source='get_review_list')
    average_rating = serializers.ReadOnlyField(source='get_average_rating')

    class Meta:
        model = Room
        fields = ['number', 'hotel', 'type', 'price', 'number_of_guests', 'average_rating', 'gallery', 'regulations',
                  'reviews']


class AllRoomSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(source="photos_of_room")
    average_rating = serializers.ReadOnlyField(source='get_average_rating')

    class Meta:
        model = Room
        fields = ['number', 'hotel', 'type', 'price', 'number_of_guests', 'average_rating', 'gallery']


class AllReservesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['id', 'room', 'day_in', 'day_out', 'number_of_guests', 'review']


class AddReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    body = serializers.CharField()

    class Meta:
        model = Review
        fields = ['rating', 'body']

    def validate(self, data):
        rating = data.get('rating')
        body = data.get('body')
        if not rating:
            raise serializers.ValidationError(detail={'rating': 'Пустое поле'})
        if not body:
            raise serializers.ValidationError(detail={'body': 'Пустое поле'})
        return data
