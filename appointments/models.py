from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('advisor', 'Advisor'),
    )

    STREAM_CHOICES = (
        ('cloud', 'Cloud Computing'),
        ('AI', 'Artificial Intelligence'),
        ('DA', 'Data Analytics'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    stream = models.CharField(max_length=50, choices=STREAM_CHOICES)

    def __str__(self):
        return self.user.username


class AvailabilitySlot(models.Model):
    advisor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.advisor.username} - {self.date} {self.time}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Waiting', 'Waiting'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_appointments')
    advisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advisor_appointments')
    slot = models.ForeignKey(AvailabilitySlot, on_delete=models.CASCADE)

    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Waiting')
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} -> {self.advisor.username} ({self.status})"