from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Student
from django.db.models import Count
from django.contrib import messages

def index(request):
    courses = Course.objects.annotate(student_count=Count('enrollment')).order_by('-student_count')
    return render(request, 'learning/index.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = Student.objects.filter(enrollment__course=course).order_by('last_name')
    all_students = Student.objects.all()

    return render(request, 'learning/course_detail.html', {
        'course': course,
        'students': students,
        'all_students': all_students,
    })

def enroll_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        if Enrollment.objects.filter(student=student, course=course).exists():
            messages.error(request, "Студент уже записан на этот курс.")
        else:
            Enrollment.objects.create(student=student, course=course)
            messages.success(request, "Студент успешно записан.")
        return redirect('course_detail', course_id=course.id)

