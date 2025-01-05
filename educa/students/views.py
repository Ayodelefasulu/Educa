from django.shortcuts import render

# imports for student registration and form creation
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# imports for course enrollment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm

# imports for displaying all courses enrolled by the students
from django.views.generic.list import ListView
from courses.models import Course

# imports for showing details of each course
from django.views.generic.detail import DetailView


# Create your views here.
# view to register students
class StudentRegistrationView(CreateView):
    template_name = "students/student/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("student_course_list")

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd["username"], password=cd["password1"])
        login(self.request, user)
        return result


# view to enroll students in courses
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data["course"]
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("student_course_detail", args=[self.course.id])


# view to display all enrolled courses
class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "students/course/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


# view to display details of a course
class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "students/course/detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if "module_id" in self.kwargs:
            # get current module
            context["module"] = course.modules.get(id=self.kwargs["module_id"])
        else:
            # get first module
            context["module"] = course.modules.all()[0]
        return context
