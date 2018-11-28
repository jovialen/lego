# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("notifications", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="notificationsetting",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("weekly_mail", "weekly_mail"),
                    ("event_bump", "event_bump"),
                    ("event_admin_registration", "event_admin_registration"),
                    ("event_payment_overdue", "event_payment_overdue"),
                    ("meeting_invite", "meeting_invite"),
                    ("penalty_creation", "penalty_creation"),
                    ("restricted_mail_sent", "restricted_mail_sent"),
                    ("company_interest_created", "company_interest_created"),
                    ("announcement", "announcement"),
                ],
                max_length=64,
            ),
        )
    ]
