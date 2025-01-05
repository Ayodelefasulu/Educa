from django.urls import path, include
from . import views

# Import for router
from rest_framework import routers

app_name = "courses"

# Router instance
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('subjects', views.SubjectViewSet)

urlpatterns = [
    #path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    #path("subjects/<pk>/", views.SubjectDetailView.as_view(), name="subject_detail"),
    path("", include(router.urls)), # router implemented
]
