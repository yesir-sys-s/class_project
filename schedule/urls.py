from django.urls import path
from .views import (
    ScheduleListView,
    ClassCreateView,
    ClassUpdateView,
    ClassDeleteView,
    HomeView,
    logout_view
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('schedule/', ScheduleListView.as_view(), name='schedule-list'),
    path('new/', ClassCreateView.as_view(), name='class-create'),
    path('<int:pk>/update/', ClassUpdateView.as_view(), name='class-update'),
    path('<int:pk>/delete/', ClassDeleteView.as_view(), name='class-delete'),
    path('logout/', logout_view, name='logout'),
]