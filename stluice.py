
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getData():

    # we are adding options to the chrome driver so that it does not open a browser window and works in the background
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)

    url= "https://jail.stluciesheriff.com/inmateSearch.php"

    # we are openning the url here
    driver.get(url)

    # Inputname in the page is called Last, so we will be using it.
    inputname = "Last"

    # We need to wait and make sure the page is loaded before we start to interact with it
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, inputname)))

    # We are sending % to the input field so that we can get all the inmates
    driver.find_element(By.NAME, inputname).send_keys("%")

    # We are pressing Enter
    driver.find_element(By.NAME, inputname).send_keys(u'\ue007')

    # There are two tables in the page, we need to get the second one. Thats why we are using index 1
    table = driver.find_elements(By.TAG_NAME, "table")[1]

    # We are getting all the rows in the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # We are creating an empty list to store the data
    inmate_list = []

    for row in rows:
        # We are getting all the columns in the row
        cells = row.find_elements(By.TAG_NAME, "td")
        # First one is the header so we need to skip it
        if len(cells) > 0:
            # We are creating an empty list to store the data for each inmate
            print(cells[0].find_element(By.TAG_NAME, "a").get_attribute("href"))
            inmatename  = cells[0].text
            profile_url = cells[0].find_element(By.TAG_NAME, "a").get_attribute("href")
            inmateid   = cells[3].text
            inmate_list.append([inmatename, profile_url, inmateid])

    # Remove first one as it is the header
    inmate_list.pop(0)

    # Write to json
    import json
    with open('inmate_list.json', 'w') as outfile:
        json.dump(inmate_list, outfile, indent=4)

    # Close the driver
    driver.quit()

    # Now we need to loop through the inmate_list and get the details. This part will take around 30 minute as there are 1000+ inmates

    for inmate in inmate_list:
        # We are getting url from the list
        url= inmate[1]

        # Making it to run in the background
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)

        driver.get(url)

        # There are two tables in the page, we need to get the second one. Thats why we are using index 1
        table = driver.find_elements(By.TAG_NAME, "table")[1]

        # We are getting all the rows in the table
        rows = table.find_elements(By.TAG_NAME, "tr")

        # We are creating an empty list to store the data
        inmate_details = []

        for row in rows:
            # We are getting all the columns in the row
            cells = row.find_elements(By.TAG_NAME, "td")
            # first one is the header so we need to skip it
            if len(cells) > 0:
                # We only need Housing info from this table
                if "Housing" in cells[1].text:
                    inmate_details.append(cells[1].text.split("\n")[6])
                    print(cells[1].text.split("\n")[6])
                    print("ok")

        # Adding inmate details to the list
        inmate.append(inmate_details[0])
        print("inmate_details", inmate_details[0])


    driver.quit()

    # write to new json
    with open('inmate_list.json', 'w') as outfile:
        json.dump(inmate_list, outfile, indent=4)

    print("Done")

def cleanData():
    # Read the json file that created during getData()
    import json
    with open('inmate_list.json') as json_file:
        inmate_list = json.load(json_file)

    # we need to remove the "Housing:  " from the last item in the list
    for inmate in inmate_list:
        inmate[3] = inmate[3].replace("Housing:  ", "")

    # count the list
    print("Total inmates: ", len(inmate_list))
    # use comprehension to get records with housing not "-". If the Housing is - it means the inmate is not in the jail, so we dont need it
    inmate_list = [inmate for inmate in inmate_list if inmate[3] != "-"]
    print("Total inmates: ", len(inmate_list))

    # we dont need profile_url so we remove it
    for inmate in inmate_list:
        inmate.pop(1)

    # we need to seperate first name and last name.. for example "Abrego Cruz, Jose Raul",266043,A3-d3 -> "Abrego Cruz", "Jose Raul",266043,A3-d3
    for inmate in inmate_list:
        inmate[0] = inmate[0].split(", ")
        lastName = inmate[0][0]
        firstName = inmate[0][1]
        # add lastName and firstName to the list
        inmate.insert(0, lastName)
        inmate.insert(1, firstName)
        # remove the old one
        inmate.pop(2)

        print(firstName, lastName)
        print("ok")

    # fixed values to be added for each inmate
    Address = "900 N. Rock Road"
    City = "Fort Pierce"
    State = "Florida"
    Zip = "34952"

    # add the fixed values to the list

    for inmate in inmate_list:
        inmate.append(Address)
        inmate.append(City)
        inmate.append(State)
        inmate.append(Zip)


    # create a csv file and include headers use pandas
    df = pd.DataFrame(inmate_list, columns = ['LastName', 'FirstName', 'InmateID', 'Housing', 'Address', 'City', 'State', 'Zip'])
    df.to_csv('inmate_list.csv', index=False)


getData()
cleanData()
