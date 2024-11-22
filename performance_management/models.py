from django.db import models
from django.conf import settings
from userauth.models import Manager, Employee


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Goal(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='employee_goals_pm', on_delete=models.CASCADE)
    description = models.TextField()
    weightage = models.DecimalField(
        max_digits=5, decimal_places=2)  # Weightage in percentage
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[(
        'Pending', 'Pending'), ('Completed', 'Completed'), ('Overdue', 'Overdue')])

    def __str__(self):
        return f"Goal for {self.employee.username} - {self.description[:20]}"


class PerformanceEvaluation(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='performance_evaluations_pm', on_delete=models.CASCADE)
    goal = models.ForeignKey(
        Goal, related_name='evaluations_pm', on_delete=models.CASCADE)
    self_rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True, help_text="Self-evaluation score (1-5 or 1-10)")
    manager_rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True, help_text="Manager rating (1-5 or 1-10)")
    final_rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True, help_text="Final aggregated rating")
    manager_feedback = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[(
        'Draft', 'Draft'), ('Submitted', 'Submitted'), ('Completed', 'Completed')], default='Draft')
    manager_id = models.ForeignKey(
        Manager, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Evaluation for {self.employee.username} | Goal: {self.goal.description[:20]}"


class PerformanceReview(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='performance_reviews_pm', on_delete=models.CASCADE)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                related_name='manager_reviews_pm', on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    self_rating = models.IntegerField(
        null=True, blank=True, help_text="Employee's self-rating (1-5)")
    manager_rating = models.IntegerField(
        null=True, blank=True, help_text="Manager's rating (1-5)")
    attachment = models.FileField(
        upload_to='attachments/', null=True, blank=True)
    review_cycle = models.CharField(max_length=50, choices=[(
        'Quarterly', 'Quarterly'), ('Annually', 'Annually')])
    status = models.CharField(max_length=20, choices=[(
        'Draft', 'Draft'), ('Submitted', 'Submitted'), ('Completed', 'Completed')], default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review: {self.title} | Employee: {self.employee.username} | Manager: {self.manager.username if self.manager else 'No Manager'}"


class Feedback(models.Model):
    evaluation = models.ForeignKey(
        PerformanceEvaluation, related_name='feedback_pm', on_delete=models.CASCADE)
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='feedback_given_pm', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='feedback_received_pm', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    feedback_type = models.CharField(max_length=20, choices=[
        ('Peer', 'Peer'),
        ('Manager', 'Manager'),
        ('Direct Report', 'Direct Report'),
    ])
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.from_user.username} to {self.to_user.username}"


class Training(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[(
        'Completed', 'Completed'), ('In Progress', 'In Progress')])
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EmployeeTraining(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='employee_trainings_pm', on_delete=models.CASCADE)
    training = models.ForeignKey(
        Training, related_name='enrollments_pm', on_delete=models.CASCADE)
    completion_status = models.CharField(max_length=20, choices=[(
        'Completed', 'Completed'), ('In Progress', 'In Progress')], default='In Progress')
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.username} | Training: {self.training.name}"


class Notification(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='notifications_pm', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50, choices=[(
        'Reminder', 'Reminder'), ('Update', 'Update'), ('Alert', 'Alert')])
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[(
        'Unread', 'Unread'), ('Read', 'Read')], default='Unread')

    def __str__(self):
        return f"Notification for {self.employee.username} | Type: {self.notification_type}"
