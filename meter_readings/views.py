from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .forms import ReadingsForm, UserCreationForm, AdminCreationForm, UserChangeForm
from .models import MeterReadings
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.db.models import Max
from django.db.models import Count
from django.core.validators import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    return HttpResponseRedirect(reverse('dashboard'))


def dashboard(request):
    return render(request, 'meter_readings/dashboard.html')


@login_required
def readings_new(request):
    if request.user.meter_readings.count() > 0:
        old_readings = MeterReadings.objects.filter(user=request.user).order_by('-publish')[0]
        readings_max_id = MeterReadings.objects.all().order_by('-id')[0]
        # if old_readings.publish.month == timezone.now().month:
        #     return render(request, 'meter_readings/month_validate.html')
        if request.method == 'POST':
            form = ReadingsForm(request.POST, instance=old_readings)
            if form.is_valid():
                readings = form.save(commit=False)
                readings.pk = readings_max_id.pk + 1
                readings.user = request.user
                readings.publish = timezone.now()
                readings.save()
                return render(request, 'meter_readings/readings_send_done.html')
        else:
            form = ReadingsForm(instance=old_readings)

    else:
        if request.method == 'POST':
            form = ReadingsForm(request.POST)
            if form.is_valid():
                readings = form.save(commit=False)
                readings.user = request.user
                readings.save()
                return render(request, 'meter_readings/readings_send_done.html')
        else:
            form = ReadingsForm()
    return render(request, 'meter_readings/readings_edit.html', {'form': form})


@login_required
def readings_list(request):
    logged_in_user = request.user
    readings = MeterReadings.objects.filter(user=logged_in_user).order_by('-publish')
    return render(request, 'meter_readings/readings_list.html', {'readings': readings})


class UserRegisterView(FormView):

    form_class = UserCreationForm
    success_url = reverse_lazy('user_register_done')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        # Функция super( тип [ , объект или тип ] )
        # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
        return super(UserRegisterView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserRegisterView, self).form_invalid(form)


def user_register_done(request):
    return render(request, 'registration/register_done.html')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_done')
    template_name = 'registration/password_change.html'


@login_required
def password_change_done(request):
    return render(request, 'registration/password_change_ok.html')


@staff_member_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'meter_readings/users_list.html', {'users': users})


@staff_member_required
def user_readings_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    readings = MeterReadings.objects.filter(user=user)
    return render(request, 'meter_readings/user_readings_list.html', {'readings': readings, 'user': user})


@staff_member_required
def user_readings_change(request, user_id, pk):
    user = get_object_or_404(User, pk=user_id)
    readings = get_object_or_404(MeterReadings, pk=pk)
    if request.method == 'POST':
        form = ReadingsForm(request.POST, instance=readings)
        if form.is_valid():
            readings = form.save(commit=False)
            readings.user = user
            readings.save()
            return redirect(reverse('user_readings_list', kwargs={'pk': user.id}))
    else:
        form = ReadingsForm(instance=readings)
    return render(request, 'meter_readings/user_readings_change.html',
                  {'form': form, 'user': user, 'readings': readings})


@staff_member_required
def user_readings_remove(request, user_id, pk):
    readings = get_object_or_404(MeterReadings, pk=pk)
    readings.delete()
    return redirect(reverse('user_readings_list', kwargs={'pk': user_id}))


@staff_member_required
def statistics(request):
    return render(request, 'meter_readings/statistics.html')


@staff_member_required
def statistics_hot(request):
    readings = MeterReadings.objects.values('user', 'user__username').annotate(hot_max=Max('hot')).order_by('-hot_max')[:3]
    return render(request, 'meter_readings/statistics_hot.html', {'readings': readings})


@staff_member_required
def statistics_cold(request):
    readings = MeterReadings.objects.values('user', 'user__username').annotate(cold_max=Max('cold')).order_by('-cold_max')[:3]
    return render(request, 'meter_readings/statistics_cold.html', {'readings': readings})


class AdminRegisterView(FormView, ):

    form_class = AdminCreationForm
    success_url = reverse_lazy('admin_creation_done')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True
        user.save()
        return super(AdminRegisterView, self).form_valid(form)

    def form_invalid(self, form):
        return super(AdminRegisterView, self).form_invalid(form)


def admin_creation_done(request):
    return render(request, 'meter_readings/admin_creation_done.html')


@login_required
def user_profile(request):
    user = request.user
    return render(request, 'meter_readings/user_profile.html', {'user': user})


@login_required
def user_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(reverse_lazy('user_profile'))
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'meter_readings/user_profile_edit.html',
                  {'form': form})
