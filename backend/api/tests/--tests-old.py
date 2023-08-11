from django.test import TestCase

from .models.user_model import Patient


class PatientTestCase(TestCase):
    def setUp(self):
        Patient.objects.create(name="Diogo", alergies="All")
        Patient.objects.create(name="Maria", alergies="peanuts")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        diogo = Patient.objects.get(name="Diogo")
        self.assertEqual(diogo.alergies, 'All')
