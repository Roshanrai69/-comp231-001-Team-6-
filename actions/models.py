from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    target_ct = models.ForeignKey(ContentType,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    target_id = models.PositiveIntegerField(blank=True,
                                            null=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    seen = models.BooleanField(default=False)  # Add a seen field

    class Meta:
        ordering = ('-created',)

    # def __str__(self):
    #     return f'{self.user.username} {self.verb} {self.target}'

    def mark_as_seen(self):  # Add a mark_as_seen method
        self.seen = True
        self.save()


