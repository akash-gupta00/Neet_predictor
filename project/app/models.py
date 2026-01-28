from django.db import models

class NeetAllotment(models.Model):
    state = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)

    # 🔴 score max 720 hota hai → Integer OK
    score = models.IntegerField(null=True, blank=True)

    # 🔥 rank 1 lakh+ ja sakta hai → BIGINT MUST
    rank = models.BigIntegerField(null=True, blank=True)

    college = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.state} | {self.score} | {self.rank}"
