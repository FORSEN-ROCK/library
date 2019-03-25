import datetime


from django.test import TestCase
from django.db.utils import IntegrityError

from open_library import models

# Create your tests here.

# Models
class AuthorTest(TestCase):
    def setUp(self):
        self.author = models.Author.objects.create(
                first_name='Max',
                last_name='Phray',
                born_date=datetime.date(1996, 1, 1),
                country='Russia',
                city='Moscow',
                language='Rus'
        )

    def test_create_now_author(self):
        """This test checks creating new book for one author"""

        author = models.Author.objects.get(first_name='Max')
        self.assertEqual(author.last_name, 'Phray')

    def test_book_count_without_books(self):
        """This test checks a property 'book_count' 
        for new author without books"""

        author = models.Author.objects.get(first_name='Max')
        self.assertEqual(author.book_count, 0)

    def test_full_name(self):
        """This test checks author full name"""

        author = models.Author.objects.get(first_name='Max')
        self.assertEqual(author.full_name, 'Max Phray ')

    def test_book_count(self):
        """This test checks a property 'book_count'
        for author with books"""

        book_one = models.Book.objects.create(
                    name='one',
                    edition=1,
                    isbn='qwerty12345',
                    publishing_house='Sp.Burg',
                    publishing_date=datetime.date(1996, 1, 1),
                    page_count=300
        )
        book_one.writed_by.add(self.author)

        book_two = models.Book.objects.create(
                    name='two',
                    edition=1,
                    isbn='qwerty12346',
                    publishing_house='Sp.Burg',
                    publishing_date=datetime.date(1996, 2, 1),
                    page_count=300
        )
        book_two.writed_by.add(self.author)

        self.assertEqual(self.author.book_count, 2)


class BookTest(TestCase):
    def setUp(self):
        today = datetime.datetime.now()

        self.book = models.Book.objects.create(
            created=datetime.date(today.year, today.month,
                                  today.day),
            name='one',
            edition=1,
            isbn='qwerty12345',
            publishing_house='Sp.Burg',
            publishing_date=datetime.date(1996, 1, 1),
            page_count=300
        )

    def test_is_not_new(self):
        """This test is negative for a property
        'is_new'"""

        self.assertEqual(self.book.is_new, False)

    def test_is_new(self):
        """This test check a property 'is_new'
        for new book"""

        today = datetime.datetime.now()
        new_book = models.Book.objects.create(
                name='new',
                edition=1,
                isbn='qwerty123456',
                publishing_house='Sp.Burg',
                publishing_date=datetime.date(today.year, 
                                    today.month, today.day),
                page_count=300
        )

        self.assertEqual(new_book.is_new, True)

    def test_adding_the_same_book(self):
        """This test checks adding the same book"""

        is_error = False

        try:
            new_book = models.Book.objects.create(
                    name='one',
                    edition=1,
                    isbn='qwerty12345',
                    publishing_house='Sp.Burg',
                    publishing_date='1996-01-01',
                    page_count=300
            )
        except IntegrityError:
            is_error = True

        self.assertEqual(is_error, True)

    def test_addig_book_with_the_other_edition(self):
        """This test checks adding new edition book"""
        
        is_error = False

        try:
            new_book = models.Book.objects.create(
                    name='one_2',
                    edition=2,
                    isbn='qwerty12345',
                    publishing_house='Sp.Burg',
                    publishing_date='1996-01-01',
                    page_count=300
            )
        except IntegrityError:
            is_error = True

        self.assertEqual(is_error, False)

    def test_cover(self):
        """This test checks cover path"""
        pass

    def test_book_with_one_author(self):
        """This test checks adding one auther"""

        alon_author = models.Author.objects.create(
                first_name='Charlse',
                last_name='Dicitson',
                born_date=datetime.date(1812, 2, 7),
                dead_date=datetime.date(1870, 6, 9),
                country='England',
                city='Gayshill',
                language='Eng'
        )

        self.book.writed_by.add(alon_author)
        self.assertEqual(self.book.writed_by.all().count(), 1)

    def test_book_with_more_one_auther(self):
        """This test checks adding more one authors"""
        first_author = models.Author.objects.create(
                first_name='Alex',
                last_name='Pushkin',
                born_date=datetime.date(1799 , 5, 26),
                dead_date=datetime.date(1837, 1, 29),
                country='Russia',
                city='Sp.Burg',
                language='Rus'
        )
        self.book.writed_by.add(first_author)

        second_author = models.Author.objects.create(
                first_name='Pushkin',
                last_name='Alex',
                born_date=datetime.date(1799 , 5, 26),
                dead_date=datetime.date(1837, 1, 29),
                country='Russia',
                city='Sp.Burg',
                language='Rus'
        )
        self.book.writed_by.add(second_author)

        self.assertEqual(self.book.writed_by.all().count(), 2)

    def test_is_not_popular(self):
        """This test is negative for a property
        'is_populare'"""
        self.assertEqual(self.book.is_popular, False)

    def test_is_popular (self):
        """This test checks a propert is_popular"""

        for i in range(1000):
            reader = models.Reader.objects.create(
                    first_name="Stiwe_%i" %(i),
                    last_name="Smit_%i" %(i),
                    middle_name='joy_%i' %(i),
                    tiket_num=i
            )

            reader.favorites_books.add(self.book)

        self.assertEqual(self.book.is_popular, True)

    def test_is_my_favorite_books(self):
        """This test checks favorite books for a persone"""
        pass
 
    def test_avalible_books_count(self):
        """This test checks a property 'avalible_books_count'"""
        for i in range(10):
            instance_book = models.BookInstance.objects.create(
                            book=self.book,
                            #is_avalible=True,
                            book_number=i,
                            order_number=10930
            )

        is_not_avalible = models.BookInstance.objects.get(
                                book_number=0
        )

        self.assertEqual(self.book.avalible_books_count, 10)

    def test_is_new_in_library(self):
        """This test checks a property 'is_new_in_library'"""
        self.assertEqual(self.book.is_new_in_library, True)

    def test_is_not_new_in_library(self):
        """This test is negative for a property 
        'is_new_in_library'"""

        old_book = models.Book.objects.create(
                    created=datetime.date(1980, 1, 1),
                    name='one',
                    edition=1,
                    isbn='qwertyu12345',
                    publishing_house='Sp.Burg',
                    publishing_date='1996-01-01',
                    page_count=300
            )

        self.assertEqual(old_book.is_new_in_library, False)


class ReaderTest(TestCase):
    def setUp(self):
        self.reader = models.Reader.objects.create(
                        first_name="Lui",
                        last_name="Amstrong",
                        middle_name="Jon",
                        tiket_num=123456,
                        language="Rus",
                        born_date = datetime.date(1989, 6, 20)
        )

    def test_full_name(self):
        """This test checks a property full_name"""
        self.assertEqual(self.reader.full_name, "Lui Amstrong Jon")

    def test_age(self):
        """This test checks a property age"""

        today = datetime.datetime.now()
        age = (datetime.date(today.year, today.month, today.day) -
               datetime.date(1989, 6, 20)).days

        self.assertEqual(self.reader.age, age)

    def test_book_at_hend(self):
        """This test checks books at hend"""

        book = models.Book.objects.create(
                    created=datetime.date(1980, 1, 1),
                    name='one',
                    edition=1,
                    isbn='qwertyu12345',
                    publishing_house='Sp.Burg',
                    publishing_date='1996-01-01',
                    page_count=300
        )

        book_instance = models.BookInstance.objects.create(
                    book=book,
                    is_avalible=True,
                    book_number=2345678,
                    order_number=10930
        )

        models.BookAtReader.objects.create(
                reader=self.reader,
                book=book_instance,
                take_date=datetime.date(1980, 1, 1),
                return_date=datetime.date(1980, 1, 14)
        )

        self.assertEqual(self.reader.book_at_hend.all()[0].book.id,
                         book_instance.id)

    def test_favorites_books(self):
        """This test checks favorites books"""

        book_one = models.Book.objects.create(
                    name='one',
                    edition=1,
                    isbn='qwerty12345',
                    publishing_house='Sp.Burg',
                    publishing_date=datetime.date(1996, 1, 1),
                    page_count=300
        )

        book_two = models.Book.objects.create(
                    name='two',
                    edition=1,
                    isbn='qwerty12346',
                    publishing_house='Sp.Burg',
                    publishing_date=datetime.date(1996, 2, 1),
                    page_count=300
        )

        self.reader.favorites_books.add(book_one)
        self.reader.favorites_books.add(book_two)

        self.assertEqual(self.reader.favorites_books.all().count(),
                         2)
        

    def test_add_new_email(self):
        """This test checks adding new email"""

        email = models.Email.objects.create(
                    email="reader_one@mail.ru",
                    reader=self.reader
        )

        self.assertEqual(
            self.reader.email_set.all()[0].email,
            "reader_one@mail.ru"
        )

    def test_add_new_phone(self):
        """This test checks adding new phone"""

        phone = models.Phone.objects.create(
                    reader=self.reader,
                    phone="88005553535"
        )

        self.assertEqual(
            self.reader.phone_set.all()[0].phone,
            "88005553535"
        )

    def test_add_new_address(self):
        """This test checks adding new address"""

        address = models.Address.objects.create(
                    reader=self.reader,
                    country="Russia",
                    city="Moscow",
                    street="Red squer",
                    house="1",
                    apartment=1
        )

        self.assertEqual(
            self.reader.address_set.all()[0].full_address,
            ("Russia, city Moscow, street" +
             " Red squer, house 1, apartment 1")
        )


class BookAtReaderTestCase(TestCase):
    def setUp(self):
        self.reader = models.Reader.objects.create(
                    first_name="Lui",
                    last_name="Amstrong",
                    middle_name="Jon",
                    tiket_num=123456,
                    language="Rus",
                    born_date = datetime.date(1989, 6, 20)
        )

        book = models.Book.objects.create(
                    name='one',
                    edition=1,
                    isbn='qwerty12345',
                    publishing_house='Sp.Burg',
                    publishing_date=datetime.date(1996, 1, 1),
                    page_count=300
        )

        self.book_instance = models.BookInstance.objects.create(
                    book=book,
                    is_avalible=True,
                    book_number=2345678,
                    order_number=10930
        )

    def test_is_not_expired(self):
        """This test is positive for 'is_expired'"""

        today = datetime.datetime.now()
        library_record = models.BookAtReader.objects.create(
                reader=self.reader,
                book=self.book_instance,
                take_date=datetime.date(
                    today.year,
                    today.month,
                    today.day
                ),
                return_date=(
                    datetime.date(today.year,
                                  today.month,
                                  today.day) + 
                    datetime.timedelta(days=14)
                )
        )

        self.assertEqual(library_record.is_expired, False)

    def test_is_expired(self):
        """This test is  negative for 'is_expired'"""

        today = datetime.datetime.now()
        library_record = models.BookAtReader.objects.create(
                reader=self.reader,
                book=self.book_instance,
                take_date=datetime.date(
                    today.year,
                    today.month,
                    today.day
                ),
                return_date=(
                    datetime.date(today.year,
                                  today.month,
                                  today.day) - 
                    datetime.timedelta(days=14)
                )
        )

        self.assertEqual(library_record.is_expired, True)