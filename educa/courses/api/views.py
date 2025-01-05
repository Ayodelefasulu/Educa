from rest_framework import generics
from courses.api.serializers import SubjectSerializer
from courses.models import Subject

# import to add django aggregate function
from django.db.models import Count

# import to add pagination
from courses.api.pagination import StandardPagination


class SubjectListView(generics.ListAPIView):
    # queryset = Subject.objects.all()
    queryset = Subject.objects.annotate(total_courses=Count("courses"))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination  # adding pagination


class SubjectDetailView(generics.RetrieveAPIView):
    # queryset = Subject.objects.all()
    queryset = Subject.objects.annotate(total_courses=Count("courses"))
    serializer_class = SubjectSerializer
