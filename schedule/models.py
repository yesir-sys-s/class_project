from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, time

class Class(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
        ('MWF', 'Monday-Wednesday-Friday'),
        ('TTH', 'Tuesday-Thursday'),
        ('TTHS', 'Tuesday-Thursday-Saturday'),
    ]
    
    DAY_MAPPING = {
        'MWF': ['MON', 'WED', 'FRI'],
        'TTH': ['TUE', 'THU'],
        'TTHS': ['TUE', 'THU', 'SAT']
    }
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=4, choices=DAY_CHOICES)  # Increased from 3 to 4
    room = models.CharField(max_length=50)
    professor = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.subject} - {self.get_day_display()}"
    
    def get_days(self):
        """Returns list of individual days for the class."""
        if self.day in self.DAY_MAPPING:
            return self.DAY_MAPPING[self.day]
        return [self.day]
    
    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError('Start time must be before end time')
            
            # Check for time conflicts across all affected days
            days_to_check = self.get_days()
            conflicts = Class.objects.filter(
                user=self.user
            ).exclude(id=self.id)
            
            for conflict in conflicts:
                conflict_days = conflict.get_days()
                # Check if any days overlap
                if any(day in conflict_days for day in days_to_check):
                    if (self.start_time <= conflict.end_time and 
                        self.end_time >= conflict.start_time):
                        raise ValidationError(
                            f'Time conflict with {conflict.subject} '
                            f'({conflict.get_day_display()}, '
                            f'{conflict.start_time.strftime("%H:%M")} - '
                            f'{conflict.end_time.strftime("%H:%M")})'
                        )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)