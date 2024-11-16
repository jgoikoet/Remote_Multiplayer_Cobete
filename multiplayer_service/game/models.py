from django.db import models
from django.utils import timezone

class Match(models.Model):
    player1_id = models.IntegerField()
    player2_id = models.IntegerField()
    player1_display_name = models.CharField(max_length=100)
    player2_display_name = models.CharField(max_length=100)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    winner_id = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
