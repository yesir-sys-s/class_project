from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Class

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect('home')

class HomeView(TemplateView):
    template_name = 'schedule/home.html'

class ScheduleListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'schedule/schedule_list.html'
    
    def get_queryset(self):
        queryset = Class.objects.filter(user=self.request.user)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(subject__icontains=search_query) |
                Q(professor__icontains=search_query) |
                Q(room__icontains=search_query)
            )
        return queryset.order_by('day', 'start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classes_by_day = {day: [] for day, _ in Class.DAY_CHOICES[:7]}  # Initialize with single days
        
        for class_obj in self.get_queryset():
            days = class_obj.get_days()
            for day in days:
                if day in classes_by_day:  # Only add to valid single days
                    classes_by_day[day].append(class_obj)
                
        context['classes_by_day'] = classes_by_day
        return context

class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    fields = ['subject', 'day', 'start_time', 'end_time', 'room', 'professor']
    template_name = 'schedule/class_form.html'
    success_url = reverse_lazy('schedule-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Class "{form.instance.subject}" was created successfully.')
            return response
        except ValidationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.user = self.request.user
        return form

class ClassUpdateView(LoginRequiredMixin, UpdateView):
    model = Class
    fields = ['subject', 'day', 'start_time', 'end_time', 'room', 'professor']
    template_name = 'schedule/class_form.html'
    success_url = reverse_lazy('schedule-list')
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = Class
    template_name = 'schedule/class_confirm_delete.html'
    success_url = reverse_lazy('schedule-list')