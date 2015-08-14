#!/usr/bin/env sh

##

echo "----"
echo "Initial Deployment Settings"
echo "----"
echo "Enable full keyboard access for all controls (e.g. enable Tab in modal dialogs)"
defaults write NSGlobalDomain AppleKeyboardUIMode -int 3

echo "Use current directory as default search scope in Finder"
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"

echo "Show Path bar in Finder"
defaults write com.apple.finder ShowPathbar -bool true

echo "Show Status bar in Finder"
defaults write com.apple.finder ShowStatusBar -bool true

echo "Expand save panel by default"
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true

echo "Expand print panel by default"
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true

echo "Enable highlight hover effect for the grid view of a stack (Dock)"
defaults write com.apple.dock mouse-over-hilte-stack -bool true

echo "Show indicator lights for open applications in the Dock"
defaults write com.apple.dock show-process-indicators -bool true

echo "Disable press-and-hold for keys in favor of key repeat"
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false

echo "Set a blazingly fast keyboard repeat rate"
defaults write NSGlobalDomain KeyRepeat -int 0.02

echo "Set a shorter Delay until key repeat"
defaults write NSGlobalDomain InitialKeyRepeat -int 12

echo "Disable disk image verification"
defaults write com.apple.frameworks.diskimages skip-verify -bool true
defaults write com.apple.frameworks.diskimages skip-verify-locked -bool true
defaults write com.apple.frameworks.diskimages skip-verify-remote -bool true

echo "Automatically open a new Finder window when a volume is mounted"
defaults write com.apple.frameworks.diskimages auto-open-ro-root -bool true
defaults write com.apple.frameworks.diskimages auto-open-rw-root -bool true
defaults write com.apple.finder OpenWindowForNewRemovableDisk -bool true

echo "Avoid creating .DS_Store files on network volumes"
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true

echo "Disable the warning when changing a file extension"
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false

echo "Show item info below desktop icons"
/usr/libexec/PlistBuddy -c "Set :DesktopViewSettings:IconViewSettings:showItemInfo false" ~/Library/Preferences/com.apple.finder.plist
echo "Enable snap-to-grid for icons"
/usr/libexec/PlistBuddy -c “Set :DesktopViewSettings:IconViewSettings:arrangeBy grid” ~/Library/Preferences/com.apple.finder.plist
/usr/libexec/PlistBuddy -c “Set :FK_StandardViewSettings:IconViewSettings:arrangeBy grid” ~/Library/Preferences/com.apple.finder.plist
/usr/libexec/PlistBuddy -c “Set :StandardViewSettings:IconViewSettings:arrangeBy grid” ~/Library/Preferences/com.apple.finder.plist

echo "Disable the “reopen windows when logging back in” option"
# This works, although the checkbox will still appear to be checked.
defaults write com.apple.loginwindow TALLogoutSavesState -bool false
defaults write com.apple.loginwindow LoginwindowLaunchesRelaunchApps -bool false
defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false

defaults write com.apple.print.PrintingPrefs “Quit When Finished” -bool true

echo "Restart the computer if it freezes"
sudo systemsetup -setrestartfreeze on

echo "Disable smart quotes as they’re annoying when typing code"
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false
echo "Disable local Time Machine snapshots"
sudo tmutil disablelocal

echo "Disable the sudden motion sensor as it’s not useful for SSDs"
sudo pmset -a sms 0


echo "Trackpad: enable tap to click for this user and for the login screen"
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true

defaults -currentHost write NSGlobalDomain com.apple.mouse.tapBehavior -int 1

defaults write NSGlobalDomain com.apple.mouse.tapBehavior -int 1

echo "Trackpad: map bottom right corner to right-click"

defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadCornerSecondaryClick -int 2

defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadRightClick -bool true

defaults -currentHost write NSGlobalDomain com.apple.trackpad.trackpadCornerClickBehavior -int 1

defaults -currentHost write NSGlobalDomain com.apple.trackpad.enableSecondaryClick -bool true

echo "Enable full keyboard access for all controls"

defaults write NSGlobalDomain AppleKeyboardUIMode -int 3

echo "Desktop as default for new finder window"

defaults write com.apple.finder NewWindowTarget -string “PfDe”

defaults write com.apple.finder NewWindowTargetPath -string “file://${HOME}/Desktop/”

echo "Show icons for hard drives, servers, and removable media on the desktop"

defaults write com.apple.finder ShowExternalHardDrivesOnDesktop -bool true

defaults write com.apple.finder ShowHardDrivesOnDesktop -bool true

defaults write com.apple.finder ShowMountedServersOnDesktop -bool true

defaults write com.apple.finder ShowRemovableMediaOnDesktop -bool true




echo "Kill affected applications"
for app in Safari Finder Dock Mail SystemUIServer; do killall "$app" >/dev/null 2>&1; done
