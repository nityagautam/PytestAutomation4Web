#!/usr/bin bash

echo "Installing Requirements ..."
python3 -m pip install -r requirements.txt

echo "Setting/Logging ENV vars ..."
echo "System Sanity checking now ..."

echo "===[TEST EXECUTION]================================"
echo "Executing the test ..."
pytest --browser=edge --url 'https://www.wikipedia.org/' -v -k test_sample

#echo "===[SUITE EXECUTION]================================"
#echo "Executing the test suite sanity ..."
#pytest --browser=edge --url 'https://www.wikipedia.org/' -v -k sanity