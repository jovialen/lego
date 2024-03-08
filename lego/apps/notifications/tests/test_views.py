from rest_framework import status

from lego.apps.notifications import constants
from lego.apps.notifications.models import Announcement
from lego.apps.users.models import AbakusGroup, User
from lego.utils.test_utils import BaseAPITestCase


class NotificationSettingsViewSetTestCase(BaseAPITestCase):
    fixtures = [
        "test_abakus_groups.yaml",
        "test_users.yaml",
        "test_notification_settings.yaml",
    ]

    def setUp(self):
        self.url = "/api/v1/notification-settings/"
        self.user = User.objects.get(pk=2)

    def test_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(
            self.url,
            {"notificationType": "weekly_mail", "enabled": True, "channels": ["email"]},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list(self):
        self.client.force_authenticate(self.user)

    def test_alternatives(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"{self.url}alternatives/")
        self.assertEqual(
            response.json(),
            {
                "notificationTypes": constants.NOTIFICATION_TYPES,
                "channels": constants.CHANNELS,
            },
        )

    def test_change_setting(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.url, {"notificationType": "weekly_mail", "enabled": True}
        )
        self.assertEqual(
            response.json(),
            {
                "notificationType": "weekly_mail",
                "enabled": True,
                "channels": ["email", "push"],
            },
        )

    def test_change_setting_defaults(self):
        """Make sure a new setting is created with correct defaults"""
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.url, {"notificationType": constants.MEETING_INVITE}
        )

        self.assertEqual(
            response.json(),
            {
                "notificationType": constants.MEETING_INVITE,
                "enabled": True,
                "channels": constants.CHANNELS,
            },
        )


class AnnouncementViewSetTestCase(BaseAPITestCase):
    fixtures = [
        "test_abakus_groups.yaml",
        "test_users.yaml",
        "test_events.yaml",
        "test_companies.yaml",
        "test_announcements.yaml",
        "test_meetings.yaml",
    ]

    def setUp(self):
        self.url = "/api/v1/announcements/"

        admin_group = AbakusGroup.objects.get(name="Webkom")
        self.authorized_user = User.objects.get(pk=9)
        self.authorized_user_2 = User.objects.get(pk=3)
        admin_group.add_user(self.authorized_user)
        admin_group.add_user(self.authorized_user_2)
        self.unauthorized_user = User.objects.get(pk=1)

        self.unsent_announcement = Announcement.objects.get(pk=5)
        self.unsent_not_own_announcement = Announcement.objects.get(pk=4)

    def test_unauthorized_create(self):
        """
        An unauthorized user should not be able to create an Announcement
        """

        self.client.force_authenticate(self.unauthorized_user)
        response = self.client.post(
            self.url, {"message": "test_message", "groups": [2], "events": [1]}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_create(self):
        """
        An authorized user should be able to create an announcement
        """

        self.client.force_authenticate(self.authorized_user)
        message = "test message"
        response = self.client.post(
            self.url,
            {"message": message, "groups": [2], "events": [1], "fromGroup": 11},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["from_group"]["id"], 11)
        self.assertEqual(response.data["message"], message)
        self.assertEqual(len(response.data["groups"]), 1)
        self.assertEqual(response.data["groups"][0]["id"], 2)
        self.assertEqual(len(response.data["events"]), 1)
        self.assertEqual(response.data["events"][0]["id"], 1)

    def test_authorized_create_from_nonexistent_group(self):
        """
        An authorized user should not be able to create an announcement with sender as
        nonexisting group
        """

        self.client.force_authenticate(self.authorized_user)
        response = self.client.post(
            self.url,
            {"message": "test_message", "groups": [2], "events": [1], "fromGroup": 999},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorized_create_invalid_recipient_groups(self):
        """
        An authorized user should not be able to create an announcement with recipient
        as invalid group
        """

        self.client.force_authenticate(self.authorized_user)
        response = self.client.post(
            self.url,
            {"message": "test_message", "groups": [59], "events": [3], "fromGroup": 11},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorized_patch(self):
        """
        It is not possible to patch an announcement
        """

        self.client.force_authenticate(self.authorized_user)
        response = self.client.patch(
            self.url,
            {
                "id": self.unsent_announcement.id,
                "message": "test_message",
                "groups": [3],
                "events": [1],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_list_own(self):
        """
        An authorized user should be able to list announcements created by self
        """

        self.client.force_authenticate(self.authorized_user_2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], 6)

    def test_authorized_detail_not_own(self):
        """
        An authorized user should not be able to list details about an announcement
        created by another user.
        """

        self.client.force_authenticate(self.authorized_user)
        response = self.client.get(f"{self.url}1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authorized_detail_own(self):
        """
        An authorized user should be able to list details about an announcement
        created by self.
        """

        self.client.force_authenticate(self.authorized_user)
        response = self.client.get(f"{self.url}5/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_list(self):
        """
        An unauthorized user should not be able to list announcements
        """

        self.client.force_authenticate(self.unauthorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_own_announcement_authorized(self):
        """
        An authorized user can send an Announcement created by self once
        """

        self.client.force_authenticate(self.authorized_user)
        response = self.client.post(f"{self.url}{self.unsent_announcement.id}/send/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(Announcement.objects.get(pk=self.unsent_announcement.id).sent)

    def test_send_not_own_announcement_authorized(self):
        """
        An authorized user can not send an Announcement created by another user
        """

        self.client.force_authenticate(self.authorized_user)
        response = self.client.post(
            f"{self.url}{self.unsent_not_own_announcement.id}/send/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_announcement_unauthorized(self):
        """
        An unauthorized user can not send an Announcement
        """

        self.client.force_authenticate(self.unauthorized_user)
        response = self.client.post(f"{self.url}{self.unsent_announcement.id}/send/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_announcement_twice(self):
        """
        An announcement can not be sent twice
        """

        self.client.force_authenticate(self.authorized_user)
        response = self.client.post(f"{self.url}{self.unsent_announcement.id}/send/")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        response = self.client.post(f"{self.url}{self.unsent_announcement.id}/send/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recipients_lookup_to_users(self):
        """
        An announcement should be sent to the specified users
        """

        announcement = Announcement.objects.get(pk=4)
        recipients = announcement.lookup_recipients()
        self.assertEqual(len(recipients), 3)

    def test_recipients_lookup_for_event(self):
        """
        Everyone registered to an event should receive the announcement
        """
        announcement = Announcement.objects.get(pk=7)
        recipients = announcement.lookup_recipients()
        self.assertEqual(len(recipients), 3)

    def test_recipients_lookup_for_event_exclude_waiting_list(self):
        """
        Everyone registered to an event, except those on waiting list,
        should receive the announcement
        """

        announcement = Announcement.objects.get(pk=8)
        recipients = announcement.lookup_recipients()
        self.assertEqual(len(recipients), 2)

    def test_recipients_lookup_for_meeting(self):
        """
        Everyone invited to a meeting should receive the announcement
        """

        announcement = Announcement.objects.get(pk=9)
        recipients = announcement.lookup_recipients()
        self.assertEqual(len(recipients), 2)

    def test_recipients_lookup_for_only_meeting_attendees(self):
        """
        Only those invited to a meeting and accepted should receive the announcement
        """

        announcement = Announcement.objects.get(pk=10)
        recipients = announcement.lookup_recipients()
        self.assertEqual(len(recipients), 1)
