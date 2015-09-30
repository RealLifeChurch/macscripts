#!/bin/bash

DOCKUTIL=/usr/local/bin/dockutil

$DOCKUTIL --remove "Mission Control" --no-restart
$DOCKUTIL --remove "Launchpad" --no-restart
$DOCKUTIL --remove "App Store" --no-restart
$DOCKUTIL --remove "TimeForce" --no-restart
$DOCKUTIL --remove "RLC Gmail" --no-restart
$DOCKUTIL --remove "Microsoft Word" --no-restart
$DOCKUTIL --remove "Microsoft Excel" --no-restart
$DOCKUTIL --remove "Calendar" --no-restart
$DOCKUTIL --remove "Pages" --no-restart
$DOCKUTIL --remove "Keynote" --no-restart
$DOCKUTIL --remove "Numbers" --no-restart
$DOCKUTIL --remove "Managed Software Center" --no-restart
$DOCKUTIL --remove 'Google Chrome' --no-restart
$DOCKUTIL --remove "Applications" --no-restart
$DOCKUTIL --remove "Downloads" --no-restart


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

$DOCKUTIL --add '/Applications/Mission Control.app' --no-restart --position 1
$DOCKUTIL --add '/Applications/Launchpad.app' --no-restart --position 2
$DOCKUTIL --add '/Applications/App Store.app' --no-restart --position 3
if [[ -n $MSC ]] ; then
  $DOCKUTIL --add '/Applications/Managed Software Center.app' --no-restart --position 4
fi
if [[ -n $GoogleChrome ]] ; then
  $DOCKUTIL --add '/Applications/Google Chrome.app' --no-restart --position 5
fi
if [[ -n $MSWord2016 ]] ; then
  $DOCKUTIL --add '/Applications/Microsoft Word.app' --no-restart --position 6
elif [[ -n $MSWord2011 ]]; then
  $DOCKUTIL --add '/Applications/Microsoft Office 2011/Microsoft Word.app' --no-restart --position 6
fi
if [[ -n $MSExcel2016 ]] ; then
$DOCKUTIL --add '/Applications/Microsoft Excel.app' --no-restart --position 7
elif [[ -n $MSWord2011 ]]; then
  $DOCKUTIL --add '/Applications/Microsoft Office 2011/Microsoft Excel.app' --no-restart --position 7
fi
if [[ -n $Pages ]] ; then
	$DOCKUTIL --add '/Applications/Pages.app' --no-restart --position 8
fi
if [[ -n $Keynote ]] ; then
	$DOCKUTIL --add '/Applications/Keynote.app' --no-restart --position 9
fi
if [[ -n $Numbers ]] ; then
	$DOCKUTIL --add '/Applications/Numbers.app' --no-restart --position 10
fi
$DOCKUTIL --add '/Applications/' --no-restart --position 11 --sort name
$DOCKUTIL --add '~/Downloads/' --position 12 --sort dateadded
