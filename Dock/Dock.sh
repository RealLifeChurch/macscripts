#!/bin/bash

DOCKUTIL=/usr/local/bin/dockutil

TimeForce=`ls /Applications/ | grep -i TimeForce`
GoogleChrome=`ls /Applications/ | grep -i Google\ Chrome`
MSWord2011=`ls /Applications/Microsoft\ Office\ 2011/ | grep -i Microsoft\ Word`
MSExcel2011=`ls /Applications/Microsoft\ Office\ 2011/ | grep -i Microsoft\ Excel`
MSWord2016=`ls /Applications/ | grep -i Microsoft\ Word`
MSExcel2016=`ls /Applications/ | grep -i Microsoft\ Excel`
Pages=`ls /Applications/ | grep -i Pages`
Keynote=`ls /Applications/ | grep -i Keynote`
Numbers=`ls /Applications/ | grep -i Numbers`
MSC=`ls /Applications/ | grep -i Managed\ Software\ Center`
$DOCKUTIL --remove /Applications/Launchpad.app
$DOCKUTIL --remove /Applications/TimeForce.app
$DOCKUTIL --remove /Applications/RLC Gmail.app
$DOCKUTIL --add '/Applications/Launchpad.app' --no-restart --position 1
if [[ -n $TimeForce ]] ; then
	$DOCKUTIL --add '/Applications/TimeForce.app' --no-restart --position 2
fi
if [[ -n $GoogleChrome ]] ; then
	$DOCKUTIL --add '/Applications/Google Chrome.app' --no-restart --position 3
fi
if [[ -n $RLCGmail ]] ; then
	$DOCKUTIL --add '/Applications/RLC Gmail.app' --no-restart --position 4
fi
if [[ -n $MSWord ]] ; then
	$DOCKUTIL --add '/Applications/Microsoft Office 2011/Microsoft Word.app' --no-restart --position 5
fi
if [[ -n $MSExcel ]] ; then
	$DOCKUTIL --add '/Applications/Microsoft Office 2011/Microsoft Excel.app' --no-restart --position 6
fi
$DOCKUTIL --add '/Applications/Calendar.app' --no-restart --position 7
if [[ -n $Pages ]] ; then
	$DOCKUTIL --add '/Applications/Pages.app' --no-restart --position 8
fi
if [[ -n $Keynote ]] ; then
	$DOCKUTIL --add '/Applications/Keynote.app' --no-restart --position 9
fi
if [[ -n $Numbers ]] ; then
	$DOCKUTIL --add '/Applications/Numbers.app' --no-restart --position 10
fi
if [[ -n $MSC ]] ; then
	$DOCKUTIL --add '/Applications/Managed Software Center.app' --no-restart --position 11
fi
$DOCKUTIL --add '/Applications/' --no-restart --position 12 --sort name
$DOCKUTIL --add '~/Downloads/' --position 13 --sort dateadded
exit 0
