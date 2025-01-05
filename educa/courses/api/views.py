from rest_framework import generics
from courses.api.serializers import SubjectSerializer, CourseSerializer
from courses.models import Subject, Course

# import to add django aggregate function
from django.db.models import Count

# import to add pagination
from courses.api.pagination import StandardPagination

# import for viewset
from rest_framework import viewsets


"""
class SubjectListView(generics.ListAPIView):
    # queryset = Subject.objects.all()
    queryset = Subject.objects.annotate(total_courses=Count("courses"))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination  # adding pagination
"""

# implementing the subject viewset; commented out SubjectListView
class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination

class SubjectDetailView(generics.RetrieveAPIView):
    # queryset = Subject.objects.all()
    queryset = Subject.objects.annotate(total_courses=Count("courses"))
    serializer_class = SubjectSerializer

# implementing course viewset
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination
