from rest_framework import serializers

from .models import Movie, Review


class FilterReviewListSerializer(serializers.ListSerializer):

	def to_representation(self, data):
		data = data.filter(parent=None)
		return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

	def to_representation(self, value):
		serializer = self.parent.parent.__class__(values, context=self.context)
		return serializer.data


class MovieListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Movie
		fields = ('title', 'tagline')


class ReviewCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Review
		fields = *__all__*


class ReviewSerializer(serializers.ModelSerializer):

	children = RecursiveSerializer(many=true)

	class Meta:
		list_serializer_class = FilterReviewListSerializer
		model = Review
		fields = ('name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):

	category = serializers.SlugRelatedField(slug_field='name', read_only=True)
	directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	acctors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	geners = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

	review = ReviewCreateSerializer(many=True)


	class Meta:
		model = Movie
		exclude = ('draft')


