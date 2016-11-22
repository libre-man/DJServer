import json

from django.contrib.auth.models import User
from django.utils import timezone
from surfer.models import Session, Channel, Client, JoinedClient

def populate_test_db():
    """ Add records to the test database. """
    user = User.objects.create_user('host', 'host@sdaas.nl', 'hostpassword') 

    # Create session.
    session_start = timezone.now()
    session_end = session_start + timezone.timedelta(hours=2)
    s = Session(host=user, name='test_session', start=session_start,
            end=session_end)
    s.save()

    # Create channels.
    c1 = Channel(session=s)
    c1.save()
    c2 = Channel(session=s)
    c2.save()

    # Create client.
    client = Client(name='client', birth_date=timezone.now())
    client.save()

    joined = JoinedClient(client=client, session=s)
    joined.save()

