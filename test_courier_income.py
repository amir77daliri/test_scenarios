from django.test import TestCase
from .models import Courier, Trip, Rewards, Deductions, DailyIncome
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from unittest.mock import patch


class TestDailyIncomeCreation(TestCase):

    def setUp(self):
        self.courier = Courier.objects.create(name="Test Courier")

    @patch('CourierIncome.models.income_calc')
    def test_transaction_rollback(self, mock_income_calc):
        # test transaction rollback
        mock_income_calc.side_effect = ValueError("Error in updating Daily income")
        test_trip_date = timezone.make_aware(datetime.now())
        trip = Trip(courier=self.courier, cost=100, trip_date=test_trip_date)
        # test save method raise error when income_calc failed
        with self.assertRaises(ValueError):
            trip.save()
        # test trip instance was rolled back
        self.assertFalse(Trip.objects.filter(courier=self.courier, cost=100, trip_date=test_trip_date).exists())

    def test_daily_income_creation(self):
        # Test successful creation of DailyIncome
        today = timezone.make_aware(datetime.now())
        Trip.objects.create(courier=self.courier, cost=Decimal('50.00'), trip_date=today)
        self.assertTrue(DailyIncome.objects.filter(courier=self.courier, date=today.date()).exists())

    def test_daily_income_update(self):
        # Test updating related object updates DailyIncome
        today = timezone.make_aware(datetime.now())
        tomorrow = timezone.make_aware(datetime.now() + timedelta(days=1))
        trip1 = Trip.objects.create(courier=self.courier, cost=Decimal('50.00'), trip_date=today)
        trip2 = Trip.objects.create(courier=self.courier, cost=Decimal('100.00'), trip_date=today)
        trip3 = Trip.objects.create(courier=self.courier, cost=Decimal('200.00'), trip_date=tomorrow)

        today_daily_income = DailyIncome.objects.get(courier=self.courier, date=today.date())
        tomorrow_daily_income = DailyIncome.objects.get(courier=self.courier, date=tomorrow.date())

        self.assertEqual(today_daily_income.day_income, trip1.cost + trip2.cost)
        self.assertEqual(tomorrow_daily_income.day_income, trip3.cost)

        # Test Deductions
        deduction = Deductions.objects.create(courier=self.courier, Amount=Decimal('-10.00'), deduction_date=today)
        today_daily_income = DailyIncome.objects.get(courier=self.courier, date=today.date())
        self.assertEqual(today_daily_income.day_income, trip1.cost + trip2.cost + deduction.Amount)

        # Test Rewards
        reward1 = Rewards.objects.create(courier=self.courier, Amount=Decimal('20.00'), reward_date=today)
        reward2 = Rewards.objects.create(courier=self.courier, Amount=Decimal('50.00'), reward_date=tomorrow)
        today_daily_income = DailyIncome.objects.get(courier=self.courier, date=today.date())
        tomorrow_daily_income = DailyIncome.objects.get(courier=self.courier, date=tomorrow.date())

        self.assertEqual(today_daily_income.day_income, trip1.cost + trip2.cost + deduction.Amount + reward1.Amount)
        self.assertEqual(tomorrow_daily_income.day_income, reward2.Amount + trip3.cost)