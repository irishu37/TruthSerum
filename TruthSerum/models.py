from django.db import models

class ImageUpload(models.Model):
    file = models.ImageField(upload_to='%Y_%m_%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
