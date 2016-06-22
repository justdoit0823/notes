

nginx on osx
============


plist file
----------

	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
		"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
		<dict>
			<key>Label</key><string>nginx</string>
			<key>Program</key><string>/usr/local/sbin/nginx</string>
			<key>KeepAlive</key><true/>
			<key>NetworkState</key><true/>
			<key>StandardErrorPath</key><string>/var/log/system.log</string>
			<key>LaunchOnlyOnce</key><true/>
		</dict>
	</plist>

plist file name
---------------

	/System/Library/LaunchDaemons/nginx.plist


launch command
--------------

	launchctl load -F /System/Library/LaunchDaemons/nginx.plist
