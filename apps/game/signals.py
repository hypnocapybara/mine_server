import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from djangorestframework_camel_case.util import camelize

from .models import Game
from .serializers import GameDetailSerializer


channel_layer = get_channel_layer()


@receiver(post_save, sender=Game)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    channel = 'game_{0}'.format(instance.pk)
    async_to_sync(channel_layer.group_send)(channel, {
        'type': 'game',
        'game': json.dumps(
            camelize(GameDetailSerializer(instance=instance).data))
    })
