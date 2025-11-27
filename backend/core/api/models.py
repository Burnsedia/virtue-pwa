from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Organization(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='organizations')

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user_owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    org_owner = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

    def clean(self):
        if not self.user_owner and not self.org_owner:
            raise ValidationError("Project must have a user or org owner.")
        if self.user_owner and self.org_owner:
            raise ValidationError("Project can't have both a user and org owner.")

    def __str__(self):
        return self.name

class Issue(models.Model):
    PRIORITY_CHOICES = [
        (1, "🔥 Urgent & Important"),
        (2, "⚠️ Urgent & Not Important"),
        (3, "🌱 Not Urgent & Important"),
        (4, "🧘 Not Urgent & Not Important"),
    ]
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    estimate_minutes = models.PositiveIntegerField(default=0)
    github_issue_number = models.IntegerField(null=True, blank=True)
    # This is a comment to force makemigrations to run
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues', null=True, blank=True)

    def __str__(self):
        return self.title

class TimeLog(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='time_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    distracted = models.BooleanField(default=False)

    def duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() // 60
        return None

