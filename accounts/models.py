from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_image(image):
    valid_extensions = ['jpg', 'jpeg', 'png', 'bmp']
    file_extension = image.name.split('.')[-1].lower()
    if file_extension not in valid_extensions:
        raise ValidationError(f'Формат файла {file_extension} не поддерживается.')
    if image.size > 2 * 1024 * 1024:
        raise ValidationError('Размер файла превышает 2 Мб.')

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='design_requests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='design_requests')
    image = models.ImageField(upload_to='requests/', blank=True, null=True, validators=[validate_image])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    comment = models.TextField(blank=True, null=True)
    completed_image = models.ImageField(upload_to='completed_requests/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
