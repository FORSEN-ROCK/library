from django.contrib import admin

from open_library import models
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'middle_name', 'born_date',
        'dead_date', 'city'
    )
    search_field = ('first_name', 'middle_name')


class ReaderAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'middle_name'
    )


class EmailAdmin(admin.ModelAdmin):
    list_display = (
        'created', 'email', 'is_active', 'reader'
    )


class PhoneAdmin(admin.ModelAdmin):
    list_display = (
        'created', 'phone', 'is_active', 'reader'
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'created', 'country', 'city', 'street',
        'house', 'is_active', 'reader'
    )


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'isbn', 'publishing_house', 'edition'
    )


class BookAtReaderAdmin(admin.ModelAdmin):
    list_display = (
        'book', 'take_date', 'return_date'
    )

admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Reader, ReaderAdmin)
admin.site.register(models.Email, EmailAdmin)
admin.site.register(models.Phone, PhoneAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.BookAtReader, BookAtReaderAdmin)