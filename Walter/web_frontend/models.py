from __future__ import unicode_literals

from django.db import models

'''
Remember the three-step guide to making model changes:

Change your models (in models.py).
Run python manage.py makemigrations to create migrations for those changes
Run python manage.py migrate to apply those changes to the database.
'''

# Create your models here.
class SugarTable(models.Model):
    username = models.CharField(max_length=40)
    blood_sugar = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField('Time taken')

    def __str__(self):
        return '[' + str(self.username) + ', ' + str(self.blood_sugar) + ', ' + str(self.timestamp) + ']'

    # timestamp = timezone.now()

    def in_ideal_range(self):
        return self.blood_sugar < 120 and self.blood_sugar > 80

    def in_danger_zone(self):
        return self.blood_sugar > 180 or self.blood_sugar < 70


def most_recent_reading(username):
     return SugarTable.objects.filter(username=username).latest('timestamp')


class PhoneNumber(models.Model):
    username = models.CharField(max_length=40)
    number = models.CharField(max_length=12)
    carrier = models.CharField(max_length=40)

    def __str__(self):
        return '[' + str(self.username) + ', ' + str(self.number) + ', ' + str(self.carrier) + ']'
