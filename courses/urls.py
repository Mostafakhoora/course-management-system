from django.urls import path
from .import views

urlpatterns = [
    path('courses/', views.course_list, name='course-list'),
    path('courses/create/', views.course_create, name='course-create'),
    path('courses/<int:pk>/',   views.course_detail, name='course-detail'),
    path('courses/<int:pk>/update/',views.course_update, name='course-update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course-delete'),
    path('enroll/', views.enroll_student, name='enroll-student'),
    path('students/', views.student_list, name='student-list'),
    path('courses/<int:pk>/students/',views.course_students,name='course-students'),
    path('dashboard/', views.web_dashboard, name='dashboard'),
    path('web/courses/', views.web_course_list, name='web-course-list'),
    path('web/courses/create/',views.web_course_create,name='web-course-create'),
    path('web/courses/<int:pk>/edit/',views.web_course_edit,name='web-course-edit'),
    path('web/courses/<int:pk>/delete/',views.web_course_delete,name='web-course-delete'),
    path('web/students/',views.web_student_list,name='web-student-list'),
    path('web/students/create/',views.web_student_create,name='web-student-create'),
    path('web/enroll/',views.web_enroll_student,name='web-enroll-student'),
    # path('api-home/', views.api_home, name='api_home'),



    ]