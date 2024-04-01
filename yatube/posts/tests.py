from django.test import TestCase

from .models import Group

print([i.title for i in Group.objects.all()])
