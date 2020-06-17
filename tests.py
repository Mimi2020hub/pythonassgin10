from django.test import TestCase
from .models import Meeting, MeetingMinutes, Resource, Event

from .views import index, getresource, getmeeting
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime

from .forms import MeetingForm, MeetingMinutesForm, ResourceForm, EventForm

#try:
#    cur.execute("LOCK TABLE mytable IN ACCESS EXCLUSIVE MODE NOWAIT")
#except psycopg2.OperationalError as e:
#    if e.pgcode == psycopg2.errorcodes.LOCK_NOT_AVAILABLE:
#        locked = True
#    else:
#        raise
#


# Create your tests here.
class MeetingTest(TestCase):
    def test_string(self):
        meet=Meeting(meetingtitle="Meeting on Firstview")
        self.assertEqual(str(meet), meet.meetingtitle)
    
    def test_table(self):
        self.assertEqual(str(Meeting._meta.db_table), 'meeting')


class MeetingMinutesTest(TestCase):
    def setup(self):
        meid=Meeting(meetingtitle='Meeting on Firstview')
        minutes=MeetingMinutes(meetingattendance = "john mimi", minutestext= "This meeting has covered the first chapter.")
        return minutes

    def test_string(self):
        minu=self.setup()
        self.assertEqual(str(minu), minu.minutestext)
    
    def test_table(self):
        self.assertEqual(str(MeetingMinutes._meta.db_table), 'meetingminutes')


class ResourceTest(TestCase):
        
    def test_string(self):
        reso=Resource(resourcename="useful link")
        self.assertEqual(str(reso),reso.resourcename)
    
    def test_table(self):
        self.assertEqual(str(Resource._meta.db_table), 'resource')



class EventTest(TestCase):
        
    def test_string(self):
        even=Event(eventtitle="watch django install video")
        self.assertEqual(str(even), even.eventtitle)
    
    def test_table(self):
        self.assertEqual(str(Event._meta.db_table), 'event')

class IndexTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class GetResourceTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('resource'))
        self.assertEqual(response.status_code, 200)

class GetMeetingTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('meeting'))
        self.assertEqual(response.status_code, 200)


class MeetingDetailTest(TestCase):
    def setup(self):
        detail=Meeting(meetingtitle='Meeting on Firstview', meetingdate='2020-05-04', meetingtime='23:38:30', meetinglocation='zoom', 
        meetingagenda='1.lecture 2.discussion')
        return detail
       
    
    def test_string(self):
        meeting=self.setup()
        self.assertEqual(str(meeting), meeting.meetingtitle)
    
    def test_table(self):
        self.assertEqual(str(Meeting._meta.db_table), 'meeting')
        

class Meeting_Form_Test(TestCase):
    def test_meetingform_is_valid(self):
        form=MeetingForm(data={'meetingtitle': "Meeting on Firstview", 'meetingdate': "2020-05-04", 'meetingtime': "23:38:30", 'meetinglocation': "zoom", 
        'meetingagenda':"1.lecture 2.discussion"})
        self.assertTrue(form.is_valid())


    def test_meetingform_minus_descript(self):
        form=MeetingForm(data={'meetingtitle': "Meeting on Firstview"})
        self.assertTrue(form.is_valid())


    def test_meetingform_empty(self):
        form=MeetingForm(data={'meetingtitle': ""})
        self.assertFalse(form.is_valid())

class MeetingMinutes_Form_Test(TestCase):
    def test_meetingminutesform_is_valid(self):
        form=MeetingMinutesForm(data={'meetingid': "Meeting on Firstview", 'meetingattendance': "john mimi", 'minutestext': "This meeting has covered the first chapter."})
        self.assertTrue(form.is_valid())


    def test_meetingminutsform_minus_descript(self):
        form=MeetingForm(data={'meetingid': "Meeting on Firstview"})
        self.assertTrue(form.is_valid())


    def test_meetingminutesform_empty(self):
        form=MeetingMinutesForm(data={'meetingid': ""})
        self.assertFalse(form.is_valid())


class Resource_Form_Test(TestCase):
    def test_resourceform_is_valid(self):
        form=ResourceForm(data={'resourcename': "useful link 2", 'resourcetype': "blog article", 'resourceurl': "https://congerprep.blogspot.com/2019/03/creating-view-to-display-data.html", 'resourceentrydate': "2020-05-07", 
        'resourceuserid':"john mary mike mimi", 'resourcedescription':"creating a view to display database"})
        self.assertTrue(form.is_valid())


    def test_resourceform_minus_descript(self):
        form=ResourceForm(data={'resourcename': "useful link 2"})
        self.assertTrue(form.is_valid())


    def test_resourceform_empty(self):
        form=ResourceForm(data={'resourcename': ""})
        self.assertFalse(form.is_valid())

class Event_Form_Test(TestCase):
    def test_eventform_is_valid(self):
        form=EventForm(data={'eventtitle': "watch django install video", 'eventlocation': "at home", 'eventdate': "2020-05-01", 'eventtime': "23:35:20", 
        'eventdescription': "Please watch the video."})
        self.assertTrue(form.is_valid())


    def test_eventform_minus_descript(self):
        form=EventForm(data={'eventtitle': "watch django install video"})
        self.assertTrue(form.is_valid())


    def test_eventform_empty(self):
        form=EventForm(data={'eventtitle': ""})
        self.assertFalse(form.is_valid())

    
    class New_Meeting_authentication_test(TestCase):
        def setUp(self):
            self.test_user=User.objects.create_user(username='testuser1', password='P@ssw0rd1')
            self.title=Meeting.objects.create(meetingtitle='Meeting on Firstview')
            self.meet = Meeting.objects.create(meetingtitle= "Meeting on Firstview", meetingdate= "2020-05-04", meetingtime= "23:38:30", meetinglocation= "zoom", meetingagenda="1.lecture 2.discussion")

        def test_redirect_if_not_logged_in(self):
            response=self.client.get(reverse('newmeeting'))
            self.assertRedirects(response, '/accounts/login/?next=/pythonclubapp/newMeeting/')

        def test_Logged_in_uses_correct_template(self):
            login=self.client.login(username='testuser1', password='P@ssw0rd1')
            response=self.client.get(reverse('newmeeting'))
            self.assertEqual(str(response.context['user']), 'testuser1')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'pythonclubapp/newmeeting.html')

    class New_MeetingMinutes_authentication_test(TestCase):
        def setUp(self):
            self.test_user=User.objects.create_user(username='testuser1', password='P@ssw0rd1')
            self.id=MeetingMinutes.objects.create(meetingid='Meeting on Firstview')
            self.minu = MeetingMinutes.objects.create(meetingid= "Meeting on Firstview", meetingattendance= "john, mimi", minutestext= "This meeting has covered the first chapter.")

        def test_redirect_if_not_logged_in(self):
            response=self.client.get(reverse('newmeetingminutes'))
            self.assertRedirects(response, '/accounts/login/?next=/pythonclubapp/newMeetingMinutes/')

        def test_Logged_in_uses_correct_template(self):
            login=self.client.login(username='testuser1', password='P@ssw0rd1')
            response=self.client.get(reverse('newmeetingminutes'))
            self.assertEqual(str(response.context['user']), 'testuser1')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'pythonclubapp/newmeetingminutes.html')
    
    class New_Resource_authentication_test(TestCase):
        def setUp(self):
            self.test_user=User.objects.create_user(username='testuser1', password='P@ssw0rd1')
            self.name=Resource.objects.create(resourcename= "useful link 2")
            self.reso = Resource.objects.create(resourcename= "useful link 2", resourcetype= "blog article", resourceurl= "https://congerprep.blogspot.com/2019/03/creating-view-to-display-data.html", resourceentrydate= "2020-05-07", 
            resourceuserid="john,mary,mike,mimi", resourcedescription= "creating a view to display database")

        def test_redirect_if_not_logged_in(self):
            response=self.client.get(reverse('newresource'))
            self.assertRedirects(response, '/accounts/login/?next=/pythonclubapp/newResource/')

        def test_Logged_in_uses_correct_template(self):
            login=self.client.login(username='testuser1', password='P@ssw0rd1')
            response=self.client.get(reverse('newresource'))
            self.assertEqual(str(response.context['user']), 'testuser1')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'pythonclubapp/newresource.html')
    
    class New_Event_authentication_test(TestCase):
        def setUp(self):
            self.test_user=User.objects.create_user(username='testuser1', password='P@ssw0rd1')
            self.title=Event.objects.create(eventtitle= "watch django install video")
            self.even = Event.objects.create(eventtitle= "watch django install video", eventlocation= "at home", eventdate= "2020-05-01", eventtime= "23:35:20", 
            eventdescription= "Please watch the video.")

        def test_redirect_if_not_logged_in(self):
            response=self.client.get(reverse('newevent'))
            self.assertRedirects(response, '/accounts/login/?next=/pythonclubapp/newEvent/')

        def test_Logged_in_uses_correct_template(self):
            login=self.client.login(username='testuser1', password='P@ssw0rd1')
            response=self.client.get(reverse('newevent'))
            self.assertEqual(str(response.context['user']), 'testuser1')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'pythonclubapp/newevent.html')
        
    
