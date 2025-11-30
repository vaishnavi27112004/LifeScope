from django.db import models
from django.contrib.auth.models import User

class LifestyleData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    steps = models.PositiveIntegerField(default=0)
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    calories = models.PositiveIntegerField(default=0)
    


    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"




