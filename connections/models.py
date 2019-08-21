from django.db import models
from authentication.models import User
# Create your models here.


class GameLinkModel(models.Model):
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_one')
    joined_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='player_two')
    game_link = models.CharField(max_length=1000)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        db_table = 'game_link'
