
from rest_framework import serializers
from .models import Course
from .models import Student



class CourseSerializer(serializers.ModelSerializer):
    enrolled_count = serializers.SerializerMethodField()
    remaining_capacity = serializers.SerializerMethodField()

    def get_enrolled_count(self, obj):
        return obj.students.count()
    def get_remaining_capacity(self, obj):
        return max(obj.capacity - obj.students.count(), 0)

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("عنوان دوره نمی‌تواند خالی باشد.")
        return value.strip()

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("قیمت نمی‌تواند منفی باشد.")
        return value

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError(
            "ظرفیت دوره باید حداقل ۱ نفر باشد."
        )
        return value
    
    class Meta:
        model = Course
        fields = '__all__'



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
