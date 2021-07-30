from decorators import *
from settings import *
import time
import config
import scrapper

@hyphen_decorator
def OSManager():
    global chrome_driver_dir

    if OS == "Windows":
        chrome_driver_dir = "ChromeDrivers/chromedriver.exe"
        print("!~The scrapper is supposed to work fine on your OS.")
        print("!~Chrome browser is expected to be installed.")
    elif OS == "Darwin":
        chrome_driver_dir = "ChromeDrivers/chromedriver"
        print("!~The scrapper is supposed to work fine on your OS ONLY if it's m1 build.")
        print("!~Chrome browser is expected to be installed.")
    else:
        print("!~The scrapper won't work on your OS!")


def run():
    OSManager()
    my_scrapper = scrapper.Scrapper(chrome_driver_dir, "Іванніков М. Т.", config.tables["kpi"][8]) #be careful when putting fio data in 
    actual_n = my_scrapper.execute()

    print(actual_n)


start_time = time.time()##
run()
print(time.time() - start_time)##