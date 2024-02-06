from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils import timezone
from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _

from django.db import models

from remember_project.settings import EMAIL_HOST_USER


class AboutPage(models.Model):
    class Meta:
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')

    about_en = RichTextUploadingField(blank=True, null=True)
    about_ru = RichTextUploadingField(blank=True, null=True)
    about_uz = RichTextUploadingField(blank=True, null=True)

    image_en = ResizedImageField(upload_to='images/about_page/',
                                 validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                                 null=True, blank=True, quality=65, force_format='JPEG')

    image_ru = ResizedImageField(upload_to='images/about_page/',
                                 validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                                 null=True, blank=True, quality=65, force_format='JPEG')

    image_uz = ResizedImageField(upload_to='images/about_page/',
                                 validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                                 null=True, blank=True, quality=65, force_format='JPEG')

    def __str__(self):
        return self.about_en


class Services(models.Model):
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    title_en = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True)

    description_en = RichTextUploadingField(null=True, blank=True)
    description_ru = RichTextUploadingField(null=True, blank=True)
    description_uz = RichTextUploadingField(null=True)

    date = models.DateField(auto_now=True, null=True)

    views = models.IntegerField(default=0, null=True, blank=True)

    icon = models.FileField(upload_to='services/services_icon/', blank=True, null=True, unique=True)

    image = ResizedImageField(upload_to='services/images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                              null=True, blank=True, quality=65, force_format='JPEG')

    image_2 = ResizedImageField(upload_to='services/images/',
                                validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                                null=True, blank=True, quality=65, force_format='JPEG')

    image_3 = ResizedImageField(upload_to='services/images/',
                                validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                                null=True, blank=True, quality=65, force_format='JPEG')
    image_4 = ResizedImageField(upload_to='services/images/',
                                validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                                null=True, blank=True, quality=65, force_format='JPEG')

    english = models.BooleanField(blank=True, default=1)

    russian = models.BooleanField(blank=True, default=1)

    uzbek = models.BooleanField(blank=True, default=1)

    def __str__(self):
        return self.title_uz

    def get_absolute_url(self):
        return reverse('tender_detail', args=[str(self.pk)])


class Graveyard(models.Model):
    class Meta:
        verbose_name = _('Graveyard')
        verbose_name_plural = _('Graveyards')

    title_en = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_uz = models.CharField(max_length=255, null=True)

    description_en = RichTextUploadingField(null=True, blank=True)
    description_ru = RichTextUploadingField(null=True, blank=True)
    description_uz = RichTextUploadingField(null=True)

    date = models.DateTimeField(auto_now=True, null=True)

    image = ResizedImageField(upload_to='graveyard/images/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg', 'webp'])],
                              null=True, blank=True, quality=65, force_format='JPEG')

    english = models.BooleanField(blank=True, default=1)

    russian = models.BooleanField(blank=True, default=1)

    uzbek = models.BooleanField(blank=True, default=1)

    def __str__(self):
        return self.title_uz

    def get_absolute_url(self):
        return reverse('cemetery_detail', args=[str(self.pk)])


class CalculateCost(models.Model):
    class Meta:
        verbose_name = _('Calculate cost')
        verbose_name_plural = _('Calculate costs')

    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True)
    service = models.ForeignKey(Services, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # for moderator
    approved = models.BooleanField(blank=True, default=False)
    reply_subject = models.CharField(max_length=255, blank=True, null=True)
    reply_message = RichTextUploadingField(max_length=1000, blank=True, null=True)
    replied_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.reply_subject and self.reply_message:
            self.replied_date = timezone.now()
            send_mail(self.reply_subject, self.reply_message, EMAIL_HOST_USER, [self.email], fail_silently=False)
            super(CalculateCost, self).save()
        else:
            super(CalculateCost, self).save()

    def __str__(self):
        return self.name


class Feedback(models.Model):
    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True)
    service = models.ForeignKey(Services, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # for moderator
    approved = models.BooleanField(blank=True, default=False)
    reply_subject = models.CharField(max_length=255, blank=True, null=True)
    reply_message = RichTextUploadingField(max_length=1000, blank=True, null=True)
    replied_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.reply_subject and self.reply_message:
            self.replied_date = timezone.now()
            send_mail(self.reply_subject, self.reply_message, EMAIL_HOST_USER, [self.email], fail_silently=False)
            super(Feedback, self).save()
        else:
            super(Feedback, self).save()

    def __str__(self):
        return self.name


class Contact(models.Model):
    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=13, null=True)
    message = RichTextUploadingField(max_length=1000, blank=True)
    received_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # for moderator
    reply_subject = RichTextUploadingField(max_length=255, blank=True, null=True)
    reply_message = RichTextUploadingField(max_length=1000, blank=True, null=True)
    replied_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.reply_subject and self.reply_message:
            self.replied_date = timezone.now()
            send_mail(self.reply_subject, self.reply_message, EMAIL_HOST_USER, [self.email], fail_silently=False)
            super(Contact, self).save()
        else:
            super(Contact, self).save()

    def __str__(self):
        return self.name
