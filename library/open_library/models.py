import datetime


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Exceptions

class BaseException(Exception):
    def __init__(self, message):
        self.message = message


class ThisBookIsAlready(BaseException):
    pass

# Models
class Author(models.Model):
    first_name = models.CharField("First name", max_length=50)
    last_name = models.CharField("Last name", max_length=50, default='')
    middle_name = models.CharField("Middle name", max_length=50,
                                   default='', null=True)
    born_date = models.DateField("Born date", null=True, default=None)
    dead_date = models.DateField("Dead date", null=True, default=None)
    country = models.CharField("Country", max_length=100, default=None)
    city = models.CharField("City", max_length=100, default=None)
    language = models.CharField("Language", max_length=100, default=None)
    biography = models.TextField("Biography", null=True, default=None)
    photo = models.FileField("Photo", default=None, null=True,
                             upload_to='uploads/author/photo/')

    @property
    def full_name(self):
        return str(' ').join(
            [self.first_name, self.last_name, self.middle_name]
        )

    @property
    def book_count(self):
        """This property retuns book count"""
        return self.book_set.all().count()


class Book(models.Model):
    created = models.DateField("Created", default=datetime.datetime.now())
    name = models.CharField("Book name", max_length=500)
    edition = models.IntegerField("Edition")
    isbn = models.CharField("ISBN", max_length=100)
    publishing_house = models.CharField("Publishing house",
                                        max_length=200)
    publishing_date = models.DateField("Publishing date",
                                        null=True, default=None)
    writed_by = models.ManyToManyField(Author)
    page_count = models.IntegerField("Page count", default=None,
                                     null=True)
    format = models.CharField("Book format", max_length=10,
                              default="A5")
    cover = models.FileField("Cover", default=None, null=True,
                             upload_to='uploads/book/cover/')

    class Meta:
        unique_together = (
                ("name", "isbn", "edition"),
        )


    @property
    def is_popular(self):
        """This property counts followers and 
        if the value is more than the threshold,
        it returns true"""
        is_popular = False
        followers_count = self.reader_set.all().count()

        if followers_count >= 1000:
            is_popular = True

        return is_popular

    @property
    def is_my_favorite(self):
        """This property return true for reader"""
        pass

    @property
    def avalible_books_count(self):
        """This property counts avalibel instance book"""
        return self.bookinstance_set.filter(is_avalible=True).count()

    @property
    def is_new(self):
        """This property ckcks the 'publishing date' and today date
        if it's less than the threshold, it returns true"""

        today = datetime.datetime.now()
        is_new = False

        publishing_days = (
            datetime.date(today.year, today.month, today.day) -
            self.publishing_date
        ).days

        if publishing_days <= 200:
            is_new = True

        return is_new

    @property
    def is_new_in_library(self):
        """This property checks the 'created' and today date
        if it's less than the threshold, it returns true"""

        today = datetime.datetime.now()
        is_new_in_library = False

        adding_days = abs(
            (datetime.date(today.year, today.month, today.day) -
            self.created).days
        )

        if adding_days <= 60:
            is_new_in_library = True

        return is_new_in_library


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete="CASCADE")
    is_avalible = models.BooleanField("Avalible", default=True)
    book_number = models.CharField("Book number", max_length=50)
    order_number = models.IntegerField("Order number")


class BookAtReader(models.Model):
    take_date = models.DateField("Take date", auto_now_add=True)
    return_date = models.DateField("Return date", null=True,
                                   default=None)
    reader = models.ForeignKey("Reader", on_delete="CASCADE")
    book = models.ForeignKey(BookInstance, on_delete="CASCADE")

    @property
    def is_expired(self):
        today = datetime.datetime.now()
        return self.return_date < datetime.date(today.year, 
                                          today.month, today.day)


class Reader(models.Model):
    first_name = models.CharField("First name", max_length=50)
    last_name = models.CharField("Last name", max_length=50)
    middle_name = models.CharField("Middle name", max_length=50)
    born_date = models.DateField("Born date", null=True, default=None)
    tiket_num = models.IntegerField("Tiket number")
    language = models.CharField("Languege", max_length=50,
                                default=None, null=True)
    is_active = models.BooleanField("Active", default=True)
    photo = models.FileField("Photo", default=None, null=True,
                             upload_to='uploads/reader/photo/')
    favorites_books = models.ManyToManyField(Book)
    book_at_hend = models.ManyToManyField(
                                BookInstance,
                                through=BookAtReader
                                #to="reader"
    )
    user = models.OneToOneField(User, on_delete="CASCADE", null=True)

    @property
    def age(self):
        today = datetime.datetime.now()
        return (datetime.date(today.year, today.month, today.day) -
                self.born_date).days

    @property
    def full_name(self):
        return str(' ').join(
            [self.first_name, self.last_name, self.middle_name]
        )


class Email(models.Model):
    created = models.DateField("Created", auto_now_add=True)
    email = models.EmailField("Email", max_length=100)
    is_active = models.BooleanField("Active", default=True)
    reader = models.ForeignKey(Reader, on_delete="CASCADE")


class Phone(models.Model):
    created = models.DateField("Created", auto_now_add=True)
    phone = models.CharField("Phone", null=False, max_length=11)
    is_active = models.BooleanField("Active", default=True)
    reader = models.ForeignKey(Reader, on_delete="CASCADE")


class Address(models.Model):
    created = models.DateField("Created", auto_now_add=True)
    country = models.CharField("Country", max_length=100)
    city = models.CharField("City", max_length=50)
    street = models.CharField("Street", max_length=100)
    house = models.CharField("House", max_length=5)
    apartment = models.CharField("Apartment", max_length=5,
                                 default="42")
    is_actual = models.BooleanField("Actual", default=False)
    is_active = models.BooleanField("Active", default=True)
    reader = models.ForeignKey(Reader, on_delete="CASCADE",
                               default=None, null=True)

    @property
    def full_address(self):
        return str(', ').join([self.country, "city " + self.city,
            "street " + self.street, "house " + self.house,
            "apartment " + self.apartment])