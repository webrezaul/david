# StLuice

Setup

Please run following commands to get your environment ready:

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt 


# How it works

Main application is: stluice.py

You can run it with following command:

python3 stluice.py

This application have 2 seperate functions:

1. getData: This is the main function to get data from given url. Here we use Selenium. I made it headless which means it will run at the background.
Plase note that since there are thousands of data, this first function takes around 30 minute to complete..
2. cleanData: Once we get the data, we clean it and append necessary updates.

# Output

Application produces two output: inmate_list.json and inmate_list.csv
Json file is produced during the getData function run and it retrieves all inmate details as it is.
CSV file is produced during the cleanData function run and it works using json file.

For the details please have a look at the comments that i embedded in the code.

# Scheduling

You can use GitHub Actions to run this job on schedule for free. You need to implement below headless driver option in the YML file.

on:
  schedule:
  - cron: '0 14 * * *' # runs at every day at 14.00pm
  workflow_dispatch:
        - uses: nanasess/setup-chromedriver@v1
        with:
          # Optional: do not specify to match Chrome's version
          chromedriver-version: '104.0.5112.79'
      - run: |
          export DISPLAY=:99
          chromedriver --url-base=/wd/hub &
          sudo Xvfb -ac :99 -screen 0 1280x1024x24 > /dev/null 2>&1 & # optional