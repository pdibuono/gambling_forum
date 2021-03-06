from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
VISIBILITY_CHOICES = (
(0, 'Public'),
(1, 'Anonymous'),
)
class Pick(models.Model):
    sport = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default=0)
    
    def __unicode__(self):
        return self.sport
    
    def get_absolute_url(self):
        return reverse("pick_detail", args=[self.id])
      
class Reply(models.Model):
    pick = models.ForeignKey(Pick)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default=0)
    
    def __unicode__(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(User)
    pick = models.ForeignKey(Pick, blank=True, null=True)
    reply = models.ForeignKey(Reply, blank=True, null=True)
    
    def __unicode__(self):
        return "%s upvoted" % (self.user.username)
    