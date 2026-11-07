
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib import messages
import courses
from .serializers import CourseSerializer,StudentSerializer
from rest_framework import status
from .models import Course, Student




@api_view(['GET'])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def course_create(request):
    serializer = CourseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'},status=404)
    
    serializer = CourseSerializer(course)
    return Response(serializer.data)

@api_view(['PUT'])
def course_update(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'},status=404)
    serializer = CourseSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def course_delete(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'},status=404)
    course.delete()
    return Response(status=204)





@api_view(['POST'])
def enroll_student(request):
    student_id = request.data.get('student_id')
    course_id = request.data.get('course_id')

    if not student_id or not course_id:
        return Response(
            {'error': 'student_id and course_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(pk=student_id)
        course = Course.objects.get(pk=course_id)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Course.DoesNotExist:
        return Response(
            {'error': 'Course not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if student.courses.filter(pk=course.pk).exists():
        return Response(
            {'error': 'Student is already enrolled'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if course.students.count() >= course.capacity:
        return Response(
            {'error': 'Course capacity is full'},
            status=status.HTTP_400_BAD_REQUEST
        )

    student.courses.add(course)

    return Response(
        {'message': 'Student enrolled successfully'},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET', 'POST'])
def student_list(request):

    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    serializer = StudentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def course_students(request, pk):

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(
            {'error': 'Course not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    students = course.students.all()
    serializer = StudentSerializer(students, many=True)

    return Response({
        'course': course.title,
        'students': serializer.data,
        'enrolled_count': students.count(),
        'remaining_capacity': max(
            course.capacity - students.count(), 0
        )
    })

@api_view(['GET'])
def course_list(request):
    courses = Course.objects.all()

    search = request.query_params.get('search')
    level = request.query_params.get('level')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    if search:
        courses = courses.filter(title__icontains=search)

    if level:
        courses = courses.filter(level=level)

    if min_price:
        courses = courses.filter(price__gte=min_price)

    if max_price:
        courses = courses.filter(price__lte=max_price)

    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


def web_dashboard(request):
    return render(request, 'courses/dashboard.html')


def web_course_list(request):
    courses = Course.objects.all()

    search = request.GET.get('search')
    level = request.GET.get('level')

    if search:
        courses = courses.filter(title__icontains=search)

    if level:
        courses = courses.filter(level=level)

    for course in courses:
        course.remaining_capacity = max(
        course.capacity - course.students.count(), 0)
    return render(request,'courses/course_list.html',{'courses': courses})

def web_course_create(request):
    if request.method == 'POST':
        serializer = CourseSerializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'دوره با موفقیت ثبت شد.')
            return redirect('web-course-list')

        return render(
            request,
            'courses/course_form.html',
            {'errors': serializer.errors}
        )

    return render(request, 'courses/course_form.html')


def web_course_edit(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(
            {'error': 'Course not found'},
            status=404
        )

    if request.method == 'POST':
        serializer = CourseSerializer(
            course,
            data=request.POST
        )

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'دوره ویرایش شد.')
            return redirect('web-course-list')

        return render(request,'courses/course_form.html',{'course': course, 'errors': serializer.errors})

    return render(
        request,
        'courses/course_form.html',
        {'course': course}
    )


def web_course_delete(request, pk):
    if request.method != 'POST':
        return Response(
            {'error': 'POST request required'},
            status=405
        )

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(
            {'error': 'Course not found'},
            status=404
        )

    course.delete()
    messages.success(request, 'دوره حذف شد.')
    return redirect('web-course-list')


from django.contrib import messages
from django.shortcuts import render, redirect

def web_student_create(request):
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'دانشجو با موفقیت ثبت شد.')
            return redirect('web-student-list')

        return render(
            request,
            'courses/student_form.html',
            {'errors': serializer.errors}
        )

    return render(request, 'courses/student_form.html')


def web_student_list(request):
    students = Student.objects.all()

    return render(
        request,
        'courses/student_list.html',
        {'students': students}
    )


def web_student_create(request):
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'دانشجو با موفقیت ثبت شد.')
            return redirect('web-student-list')

        return render(
            request,
            'courses/student_form.html',
            {'errors': serializer.errors}
        )

    return render(request, 'courses/student_form.html')


def web_enroll_student(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    errors = None

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')

        try:
            student = Student.objects.get(pk=student_id)
            course = Course.objects.get(pk=course_id)

            if student.courses.filter(pk=course.pk).exists():
                errors = 'این دانشجو قبلاً در این دوره ثبت‌نام کرده است.'

            elif course.students.count() >= course.capacity:
                errors = 'ظرفیت این دوره تکمیل شده است.'

            else:
                student.courses.add(course)
                messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
                return redirect('web-student-list')

        except (Student.DoesNotExist, Course.DoesNotExist):
            errors = 'دانشجو یا دوره انتخاب‌شده معتبر نیست.'

    return render(
        request,
        'courses/enroll_form.html',
        {
            'students': students,
            'courses': courses,
            'errors': errors,
        }
    )


def api_home(request):
    return render(request, 'courses/api_home.html')
