import time
import json

from django.test import TestCase, Client

from .testing_utilities import populate_test_db
from surfer import models as s


class ControllerApiTests(TestCase):

    def setUp(self):
        populate_test_db()
