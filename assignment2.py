import argparse
import urllib.request
import logging
from datetime import datetime

def downloadData(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

def processData(data):
    personData = {}
    logger = logging.getLogger('assignment2')
    lines = data.strip().split('\n')

    for linenum, line in enumerate(lines[1:], start=2):
        try:
            id_str, name, birthday_str = line.strip().split(',')
            id = int(id_str)
            birthday = datetime.strptime(birthday_str, "%d/%m/%Y")
            personData[id] = (name, birthday)
        except Exception:
            logger.error(f"Error processing line #{linenum} for ID #{id_str}")

    return personData

def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y%m%d')}")

    else:
        print("No user found with that id")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='URL to the CSV data file')
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log', level=logging.ERROR)

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    personData = processData(csvData)

    while True:
        try:
              user_input = int(input("Enter an ID number (<= 0 to exit): "))
              if user_input <= 0:
                   print("Exiting program.")
                   break
              displayPerson(user_input, personData)
        except ValueError:
                print("Please enter a valid integer.")

if __name__ == '__main__':
     main()

