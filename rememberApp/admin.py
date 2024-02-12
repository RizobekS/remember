from django.contrib import admin
from .models import User, AboutPage, Services, Contact, CalculateCost, Feedback, Graveyard, Gallery, MyServices


class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['about_en', 'about_ru', 'about_uz']


class ServicesAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_uz', 'title_ru', 'value',
                    'english', 'russian', 'uzbek', 'date', 'views']

    list_editable = ['value', 'english', 'russian', 'uzbek', 'views']

    fields = ['title_uz', 'description_uz', 'title_en', 'description_en', 'title_ru', 'description_ru', 'value',
              'image', 'image_2', 'image_3', 'image_4', 'icon', 'views', 'english', 'russian', 'uzbek']

    search_fields = ['title_en', 'title_uz', 'title_ru']


class GraveyardAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'title_uz', 'description_ru', 'description_uz', 'date']
    search_fields = ['title_ru', 'title_uz']


class CalculateCostAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'service', 'date', 'approved']
    search_fields = ['service__title_ru', 'name', 'email', 'phone']
    list_editable = ['approved']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'service', 'date', 'approved']
    search_fields = ['service__title_ru', 'name', 'email', 'phone']
    list_editable = ['approved']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'message', 'received_date', 'replied_date', 'reply_subject', 'reply_message']
    search_fields = ['name', 'phone', 'email', 'message']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'title_ru', 'title_uz', 'image', 'type', 'date']
    search_fields = ['title_en', 'title_ru', 'title_uz']


admin.site.site_header = "Remember Me"
admin.site.register(User)
admin.site.register(MyServices)
admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Graveyard, GraveyardAdmin)
admin.site.register(CalculateCost, CalculateCostAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Gallery, GalleryAdmin)
