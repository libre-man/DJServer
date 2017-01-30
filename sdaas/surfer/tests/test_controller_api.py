import time
import json
import tempfile

from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from surfer.models import Session, Channel, ControllerPart, ControllerPartOption, File


class ControllerApiTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.populate_db()

    def populate_db(self):
        user = User.objects.create_user(
            'host', 'host@sdaas.nl', 'hostpassword')
        user.save()
        self.session = Session(host=user, name='test_session',
                               join_code='test', start=timezone.now(), end=timezone.now())

        self.session.save()

        self.channel = Channel.objects.create_channel(
            self.session, name='test')
        self.channel.save()

    def test_im_alive_correct(self):
        self.assertFalse(self.channel.is_initialized)

        request = {
            "id": self.channel.id,
            "options": {
                "Picker": {
                    "NCAPicker": {
                        "doc": {
                            "short": "A short description",
                            "long": "A long description with\nnewlines"
                        },
                        "parts": {
                            "arg1": {
                                "fixed": False,
                                "required": True,
                                "doc": "You should use this like this!"
                            }
                        }
                    }
                },
                "Controller": {
                    "SimpleController": {
                        "doc": {
                            "short": "A short description",
                            "long": "A long description with\nnewlines"
                        },
                        "parts": {
                            "arg3": {
                                "fixed": True,
                                "required": False,
                                "doc": ""
                            }
                        }
                    }
                }
            }
        }

        response = self.client.post(
            '/im_alive/', json.dumps(request), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        channel = Channel.objects.get(pk=self.channel.id)
        self.assertTrue(channel.is_initialized)

        # Test part 1
        picker_part1 = ControllerPart.objects.filter(name='NCAPicker')
        self.assertEqual(len(picker_part1), 1)
        picker_part1 = picker_part1[0]
        self.assertEqual(picker_part1.category, ControllerPart.PICKER)
        self.assertEqual(picker_part1.short_doc, 'A short description')
        self.assertEqual(picker_part1.long_doc,
                         'A long description with\nnewlines')

        # Test option1
        picker_part1_option1 = ControllerPartOption.objects.filter(
            name='arg1', controller_part=picker_part1)
        self.assertEqual(len(picker_part1_option1), 1)
        picker_part1_option1 = picker_part1_option1[0]

    def test_im_alive_empty(self):
        response = self.client.post(
            '/im_alive/', json.dumps({}), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_music_processed(self):
        f = tempfile.NamedTemporaryFile(suffix='.mp3')
        uploaded_file = SimpleUploadedFile(f.name, f.read())
        File.objects.create_file(channel=self.channel, upload=uploaded_file)
        music = File.objects.latest('id')

        self.assertFalse(music.is_processed)

        request = {'id': music.id}
        response = self.client.post(
            '/music_processed/', json.dumps(request), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(File.objects.get(pk=music.id).is_processed)
