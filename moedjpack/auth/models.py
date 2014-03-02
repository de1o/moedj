from django.db import models


class WeiboAuth(models.Model):
    access_token = models.CharField(max_length=100)
    access_token_secret = models.CharField(max_length=100)
    expires_in = models.IntegerField()
    source = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20)
    uid = models.CharField(max_length=32)

    def __unicode__(self):
        return self.access_token
