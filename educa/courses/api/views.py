from rest_framework import generics
from courses.api.serializers import SubjectSerializer, CourseSerializer
from courses.models import Subject, Course

# import to add django aggregate function
from django.db.models import Count

# import to add pagination
from courses.api.pagination import StandardPagination

# import for viewset
from rest_framework import viewsets

# import for building custom API views
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

# import for basic authentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# import to add addtional actions to viewset
from rest_framework.decorators import action


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

    # implementation of additional action
    # after implement the additional action,
    # the CourseEnrollView class will be commented out below
    @action(
        detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

# implementing custom API views
"""
class CourseEnrollView(APIView):
    # implementing basic authentication
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})
"""
