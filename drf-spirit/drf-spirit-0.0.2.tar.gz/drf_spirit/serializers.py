from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .fields import UserReadOnlyField
from .models import Topic, Category, Comment
from .relations import PresentableSlugRelatedField


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryLiteSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'slug', 'color')


class TopicSerializer(ModelSerializer):

    user = UserReadOnlyField()
    category = PresentableSlugRelatedField(queryset=Category.objects.all(),
                                           presentation_serializer=CategoryLiteSerializer,
                                           slug_field='slug')

    class Meta:
        model = Topic
        fields = '__all__'
        # TODO:: refactor after deciding about globally pinned.
        read_only_fields = ('is_pinned',)


class CommentSerializer(ModelSerializer):

    user = UserReadOnlyField()

    class Meta:
        model = Comment
        fields = '__all__'
