from django.contrib.auth import get_user_model
from django.db import models


class UserActions(models.Model):
    route = models.TextField()
    method = models.TextField()
    data = models.TextField()
    ip_address = models.GenericIPAddressField()
    token = models.TextField()
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, editable=False)
    accepted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User Actions'

    def __str__(self):
        return f"(IP Address=={self.ip_address}) with method {self.method} on route {self.route}"    


class Limit(models.Model):
    CONDITION_CHOICES = (
        ('>', 'Greater Than'),
        ('<', 'Less Than'),
        ('==', 'Equal To'),
        ('>=', 'Greater Than or Equal To'),
        ('<=', 'Less Than or Equal To')
    )
    OPERATOR_CHOICES = (
        ('sum', 'SUM'),
        ('count', 'COUNT'),
        ('max', 'MAX'),
        ('min', 'MIN'),
        ('ctd', 'COUNT DISTINCT')
    )
    action = models.TextField(blank=True)
    action_method = models.TextField()
    metric = models.TextField(blank=True)
    metric_method = models.TextField()
    metric_prop = models.TextField(default='id')
    time_frame = models.DurationField()
    operation = models.TextField(choices=OPERATOR_CHOICES)
    value = models.IntegerField(default=0)
    condition = models.TextField(choices=CONDITION_CHOICES)
    error_message = models.TextField(default='An Error Occurred')
    error_code = models.PositiveIntegerField(default=404)

    def get_operation(self):
        return {
            'sum': sum,
            'count': len,
            'max': max,
            'min': min,
            'ctd': lambda x: len(set(x))
        }[self.operation]

    def get_comparison(self):
        return {
            '>': int.__gt__,
            '<': int.__lt__,
            '==': int.__eq__,
            '>=': int.__ge__,
            '<=': int.__le__
        }[self.condition]

    def __str__(self):
        return f"{self.operation}('{self.metric}', {self.time_frame}) {self.condition} {self.value}"
