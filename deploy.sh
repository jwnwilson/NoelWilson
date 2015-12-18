#!/bin/bash

# Simple deploy script will check debug is set to false update the appcache file
# and increase the version number defore deploying to GAE

# contains(string, substring)
#
# Returns 0 if the specified string contains the specified substring,
# otherwise returns 1.
contains_result=-1
contains() {
    string="$1"
    substring="$2"
    if test "${string#*$substring}" != "$string"
    then
        contains_result=1    # $substring is in $string
    else
        contains_result=0    # $substring is not in $string
    fi
}

cd "$(dirname "$0")"
settings_file="notifications/settings.py"
settings_debug_line=16
app_file=app.yaml
target_app_id="google.com:emt-notifications"
#appcache_file=static/emt-tool.appcache

echo ""
files_check_ok=1

# Check all debug set to false
# Check settings_file

app_dev=`sed '9!d' $app_file`
settings_debug=`sed "$settings_debug_line!d" $settings_file`

if [ "$app_dev" == "application: $target_app_id" ]
then
	if [ "$settings_debug" != "DEBUG = False" ]
    then
		echo "DEBUG set to True please run .version_up.sh"
		files_check_ok=0
	else
		echo "settings set to DEBUG = False"
	fi
else
    echo "Deploying to $target_app_id not checking tito debug setting"
fi
echo ""

echo ""
if [ "$files_check_ok" == "1" ]
then
    # Deploy
    echo "Deploying application to production."
    appcfg.py update --oauth2 .
else
    echo "Files require changes before deploying, possible changes needed to debug settings in files please check settings"
fi