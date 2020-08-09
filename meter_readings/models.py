from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError


class MeterReadings(models.Model):
    hot = models.PositiveIntegerField(verbose_name='Горячая вода', validators=[MaxValueValidator(99999), MinValueValidator(0)])
    cold = models.PositiveIntegerField(verbose_name='Холодная вода', validators=[MaxValueValidator(99999), MinValueValidator(0)])
    publish = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, related_name='meter_readings', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-publish',)

    # def clean(self):
    #     old_readings = MeterReadings.objects.filter(user=self.user).order_by[0]
    #     old_hot = old_readings.hot
    #     if self.hot < old_hot:
    #         return ValidationError('Введенное значение меньше предыдущего')

    def __str__(self):
        return self.user
