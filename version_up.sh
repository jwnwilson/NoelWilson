#!/bin/bash

# Simple version up script to set all debug option to false and version up
# the tool before deploying it, for use in creating a new master commit

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

# Script variables
settings_file=noelwilson/settings.py
settings_debug_line=5
appcache_file=app.yaml
files_check_ok=1

# parse version info
VERSION=`git describe --abbrev=0 --tags`
PREV_VERSION=$VERSION
VERSION="${VERSION//v/}"
arrVERSION=(${VERSION//./ })
MINOR=${arrVERSION[2]}
MINOR=$((MINOR+1))
arrVERSION[2]=$MINOR
arrVERSION[3]=`date +%Y%m%d`
VERSION="$(printf ".%s" "${arrVERSION[@]}")"
PYVERSION="${VERSION:1}"
VERSION="v${VERSION:1}"
ANNOTATION=$1

if [ "$ANNOTATION" == "" ]
then
    echo "No annotaion supplied for comment please supply annotion then re-run script."
    exit
fi

cd "$(dirname "$0")"
echo ""

# Check all debug set to false
file_debug=`sed "$settings_debug_line!d" $settings_file`
if [ "$file_debug" != "DEBUG = False" ]
then
    echo "DEBUG set to True attempting to set to False"
    cp $settings_file "noelwilson/settings_temp.py"
    sed -i '' 's/DEBUG = True/DEBUG = False/' "noelwilson/settings_temp.py"
    line_var=`sed "$settings_debug_line!d" "noelwilson/settings_temp.py"`
    if [ "$line_var" == "DEBUG = False" ]
    then
        echo "settings set to DEBUG = False"
        mv  "noelwilson/settings_temp.py" $settings_file
    else
        echo "Unexpected results no changes make to settings"
        rm "noelwilson/settings_temp.py"
        files_check_ok=0
    fi
else
    echo "Settings set to DEBUG = False"
fi
echo ""

echo "Updating version info"
echo "Previous version: $PREV_VERSION"
echo "Current version: $VERSION"

# Version up appcache file
echo ""
if [ "$files_check_ok" == "1" ]
then
    # Version up app.yaml
    version="${VERSION//./-}"
    #echo "Setting version from git: $version"
    echo "Setting app.yaml file version: $version"
    sed -i '' "2s/.*/version: $version/" app.yaml
    echo ""
else
    # If we found debug = true and were unable to fix warn and exit
    echo "Files require changes before deploying, possible changes needed to debug settings in files please check tito.py and travelCalendarExt.js"
    exit
fi

echo "Setting version for version.py: $PYVERSION"
sed -i '' "1s/'.*'/'$PYVERSION'/" ./version.py

# Create a new commit with changes
git commit -am "$ANNOTATION"

echo "New version: $VERSION"
echo "Annoation for tag: $ANNOTATION"

# Create new tag
git tag -a "$VERSION" -m "$ANNOTATION"

version=`git describe --abbrev=0 --tags`
version="'${version//v/}'"

echo "Code commited and tagged as version: $VERSION"
