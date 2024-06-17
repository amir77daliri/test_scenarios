
# this test senario is for my university project 

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .serializers import ClassroomSerializer


class SerializerTest(TestCase):
    def test_capacity_validation_valid_value(self):
        # Test valid capacity value (>= 5)
        serializer = ClassroomSerializer(data={'capacity': 10, 'area': 50, 'name' :'test name'})
        self.assertTrue(serializer.is_valid())

    def test_capacity_validation_invalid_value(self):
        # Test invalid capacity value (< 5)
        serializer = ClassroomSerializer(data={'capacity': 3, 'area': 50,'name' :'test name'})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertFalse(serializer.is_valid())

    def test_area_validation_valid_value(self):
        # Test valid area value (>= 0)
        serializer = ClassroomSerializer(data={'capacity': 10, 'area': 50,'name' :'test name'})
        self.assertTrue(serializer.is_valid())

    def test_area_validation_invalid_value(self):
        # Test invalid area value (< 0)
        serializer = ClassroomSerializer(data={'capacity': 10, 'area': -10,'name' :'test name'})
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertFalse(serializer.is_valid())

    def test_serializer_with_valid_data(self):
        # Test serializer with valid data
        data = {'capacity': 10, 'area': 50,'name' :'test name'}
        serializer = ClassroomSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        classroom_obj = serializer.save()

        # Check if serializer saves the object correctly
        self.assertEqual(classroom_obj.capacity, data['capacity'])
        self.assertEqual(classroom_obj.area, data['area'])

    def test_serializer_with_invalid_data(self):
        # Test serializer with invalid data
        data = {'capacity': 3, 'area': -10,'name' :'test name'}
        serializer = ClassroomSerializer(data=data)
        self.assertFalse(serializer.is_valid())
