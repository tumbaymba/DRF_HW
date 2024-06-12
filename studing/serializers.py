from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from studing.models import Course, Lesson, Subscription
from studing.validators import UrlValidator

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='video_url')]

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lesson_set.count()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        if Subscription.objects.filter(user=user, course=instance).exists():
            return True
        return False


    class Meta:
        model = Course
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())

    class Meta:
        model = Course
        fields = '__all__'
