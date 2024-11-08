from django.db import models
from django.conf import settings

class PerformanceReview(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='performance_reviews', on_delete=models.CASCADE)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='manager_reviews', on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    self_rating = models.IntegerField(null=True, blank=True, help_text="Employee's self-rating (1-5)")
    manager_rating = models.IntegerField(null=True, blank=True, help_text="Manager's rating (1-5)")
    attachment= models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False) 
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    review_cycle = models.CharField(max_length=50, choices=[('Quarterly', 'Quarterly'), ('Annually', 'Annually')])
    status = models.CharField(max_length=20, choices=[('Draft', 'Draft'), ('Submitted', 'Submitted'), ('Completed', 'Completed')], default='Draft')

    def __str__(self):
        return f"Review: {self.title} | Employee: {self.employee.username()} | Manager: {self.manager.username() if self.manager else 'No Manager'}"

# class PerformanceReview(models.Model):
#     employee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='performance_reviews', on_delete=models.CASCADE)
#     manager = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='manager_reviews', on_delete=models.SET_NULL)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     deadline = models.DateField(null=True, blank=True)
#     self_rating = models.IntegerField(null=True, blank=True, help_text="Employee's self-rating (1-5)")
#     manager_rating = models.IntegerField(null=True, blank=True, help_text="Manager's rating (1-5)")
    
#     # New fields
#     goals = models.ManyToManyField(Goal, blank=True, related_name='associated_reviews', help_text="Goals associated with this review.")
#     final_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Final calculated rating.")
#     training_recommendations = models.ManyToManyField(Training, blank=True, related_name='recommended_reviews', help_text="Trainings recommended for this review.")
#     employee_comments = models.TextField(blank=True, null=True, help_text="Employee's additional comments.")
#     manager_comments = models.TextField(blank=True, null=True, help_text="Manager's additional comments.")
    
#     attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_approved = models.BooleanField(default=False)
#     review_cycle = models.CharField(max_length=50, choices=[('Quarterly', 'Quarterly'), ('Annually', 'Annually')])
#     status = models.CharField(max_length=20, choices=[('Draft', 'Draft'), ('Submitted', 'Submitted'), ('Completed', 'Completed')], default='Draft')

#     def __str__(self):
#         return f"Review: {self.title} | Employee: {self.employee.username()} | Manager: {self.manager.username() if self.manager else 'No Manager'}"
