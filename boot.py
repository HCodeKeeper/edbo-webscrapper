from decorators import *
import config
import platform
import os

#Identifying OS for driver selecting
OS = platform.system()
os.chmod('ChromeDrivers/chromedriver', 0o0755)
chrome_driver_dir = None

api = None


#initializating api
@hyphen_decorator
def OSManager():
    global chrome_driver_dir

    if OS == "Windows":
        chrome_driver_dir = config.drivers["Win"]
        print("!~The scrapper is supposed to work fine on your OS.")
        print("!~Chrome browser is expected to be installed.")
        request_result = init(chrome_driver_dir)
    elif OS == "Darwin":
        chrome_driver_dir = config.drivers["Mac-M1"]
        print("!~The scrapper is supposed to work fine on your OS ONLY if it's m1 build.")
        print("!~Chrome browser is expected to be installed.")
        request_result = init(chrome_driver_dir)
    else:
        print("!~The scrapper won't work on your OS!")
        request_result = False

    return request_result

def init(driver_dir):
    global api
    import api
    api = api.Api 
    api.CHROME_DRIVER_DIR = driver_dir
    return True


print(OSManager())