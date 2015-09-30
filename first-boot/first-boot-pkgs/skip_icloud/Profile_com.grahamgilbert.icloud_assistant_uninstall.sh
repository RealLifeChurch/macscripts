#!/bin/sh

/usr/bin/profiles -R -p com.grahamgilbert.icloud_assistant
/bin/rm -f /Library/reallifechurch/Profiles/com.grahamgilbert.icloud_assistant.mobileconfig
/usr/sbin/pkgutil --forget org.realllifechurch.Profile_com.grahamgilbert.icloud_assistant
