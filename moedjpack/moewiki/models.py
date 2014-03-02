from django.db import models
import datetime
from django.utils import timezone

class WikiItems(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=256)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.title

    def was_add_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(hours=24)


class AlreadlyRetweeted(models.Model):
    tid = models.CharField(max_length=32)
    source = models.CharField(max_length=20)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.tid

    def was_add_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(hours=2)


class RecentUpdateItems(models.Model):
    VERIFYING_NEW = 0
    VERIFIED = 1
    EDITED = 2
    SENT = 3
    ITEM_STATE = (
        (VERIFYING_NEW, 'VerifyingNewItem'),
        (VERIFIED, 'VerifiedItem'),
        (EDITED, 'Edited'),
        (SENT, 'Sent'),
    )

    title = models.CharField(max_length=128)
    itemState = models.IntegerField(default=EDITED, choices=ITEM_STATE)
    changeTime = models.DateTimeField()
    sentTime = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class MoePadConfig(models.Model):

    SinaAppKey = models.CharField(max_length=32, blank=True)
    sinaAppSecret = models.CharField(max_length=64, blank=True)
    TencentAppKey = models.CharField(max_length=32, blank=True)
    TencentAppSecret = models.CharField(max_length=64, blank=True)
    MoeWebsite = models.CharField(max_length=128)
    feedurl = models.CharField(max_length=512)
    mail_from = models.CharField(max_length=64, blank=True)
    mail_to = models.CharField(max_length=64, blank=True)
    smtpserver = models.CharField(max_length=64, blank=True)
    mail_user = models.CharField(max_length=50, blank=True)
    mail_passwd = models.CharField(max_length=50, blank=True)
    mcport = models.IntegerField(default=11211)
    sameItemInterval = models.IntegerField(default=24)
    generalRetainTime = models.IntegerField(default=48)