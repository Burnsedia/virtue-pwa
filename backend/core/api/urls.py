from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('organizations', OrganizationViewSet)
router.register('projects', ProjectViewSet)
router.register('issues', IssueViewSet)
router.register('timelogs', TimeLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

