from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Appointment, AvailabilitySlot
from .forms import AppointmentForm

def role_redirect(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')

    if user.profile.role == 'advisor':
        return redirect('advisor_dashboard')

    if user.profile.role == 'student':
        return redirect('student_dashboard')

    return redirect('login')


@login_required
def student_dashboard(request):
    appointments = Appointment.objects.filter(student=request.user)
    return render(
        request,
        'appointments/student_dashboard.html',
        {'appointments': appointments}
    )


@login_required
def book_appointment(request):
    student_stream = request.user.profile.stream

    advisors = User.objects.filter(
        profile__stream=student_stream,
        profile__role='advisor'
    )

    slots = AvailabilitySlot.objects.filter(advisor__in=advisors)

    form = AppointmentForm(request.POST or None)
    form.fields['slot'].queryset = slots

    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)
        appointment.student = request.user
        appointment.advisor = appointment.slot.advisor
        appointment.status = "Waiting"
        appointment.save()
        return redirect('student_dashboard')

    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, student=request.user)

    if appointment.status != 'Waiting':
        return redirect('student_dashboard')

    student_stream = request.user.profile.stream

    advisors = User.objects.filter(
        profile__stream=student_stream,
        profile__role='advisor'
    )

    form = AppointmentForm(request.POST or None, instance=appointment)
    form.fields['slot'].queryset = AvailabilitySlot.objects.filter(advisor__in=advisors)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('student_dashboard')

    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, student=request.user)

    if appointment.status == 'Waiting':
        appointment.delete()

    return redirect('student_dashboard')


@login_required
def advisor_dashboard(request):
    waiting = Appointment.objects.filter(advisor=request.user, status='Waiting')
    approved = Appointment.objects.filter(advisor=request.user, status='Approved')
    rejected = Appointment.objects.filter(advisor=request.user, status='Rejected')

    return render(
        request,
        'appointments/career_advisor_dashboard.html',
        {
            'waiting': waiting,
            'approved': approved,
            'rejected': rejected,
        }
    )


@login_required
def approve_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, advisor=request.user)
    appointment.status = 'Approved'
    appointment.comments = request.POST.get('comments', '')
    appointment.save()
    return redirect('advisor_dashboard')


@login_required
def reject_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, advisor=request.user)
    appointment.status = 'Rejected'
    appointment.comments = request.POST.get('comments', '')
    appointment.save()
    return redirect('advisor_dashboard')