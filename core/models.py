from django.db import models
# Create your models here
class AbstractModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
class Media(AbstractModel):
    video = models.FileField(upload_to='video',null=True,blank=True,unique=False)
    audio = models.FileField(upload_to='audio',null=True,blank=True,unique=False)
    text = models.FileField(upload_to='text',null=True,blank=True,unique=False)

    def __str__(self):
        return self.video.name
