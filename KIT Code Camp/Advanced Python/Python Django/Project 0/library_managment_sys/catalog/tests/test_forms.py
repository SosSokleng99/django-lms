import datetime
from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm

class RenewBookFormTest(TestCase):

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        print(date)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
    
    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=3) - datetime.timedelta(days=2)
        print(date)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())
