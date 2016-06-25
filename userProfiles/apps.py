"""
this was created when I added the app
"""

from __future__ import unicode_literals

from django.apps import AppConfig


class userProfilesConfig(AppConfig):
    name = 'userProfiles'
    verbose_name = 'User Profiles'

    def ready(self):

    	# import signal handlers
    	import userProfiles.signals