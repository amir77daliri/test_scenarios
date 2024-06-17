# test celery tasks with pytest
import pytest
from unittest.mock import patch
from django.utils import timezone
from django.contrib.auth.models import User
from task_app.tasks import send_due_task_reminders
from task_app.models import Task
from datetime import timedelta

@pytest.mark.django_db
class TestCeleryTasks:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(username='my_username', email='test@gmail.com')
        self.task_due_soon = Task.objects.create(
            title='Due Soon Task',
            assigned_to=self.user,
            due_date=timezone.now() + timedelta(hours=23)
        )
        self.task_not_due_soon = Task.objects.create(
            title='Not Due Soon Task',
            assigned_to=self.user,
            due_date=timezone.now() + timedelta(days=2)
        )

    @patch('task_app.tasks.send_mail')
    def test_send_due_task_reminders(self, mock_send_mail):
        send_due_task_reminders()

        # Check that an email was sent for the task due soon
        mock_send_mail.assert_called_once_with(
            'Task Due Reminder',
            f'The task "{self.task_due_soon.title}" is due soon.',
            'website@gmail.com',
            [self.task_due_soon.assigned_to.email],
        )

        # Ensure no email was sent for the task not due soon
        self.assertEqual(mock_send_mail.call_count, 1)
