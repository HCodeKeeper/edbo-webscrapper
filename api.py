import scrapper
from decorators import *


class Api:
    #Consts
    CHROME_DRIVER_DIR = None


    def run_filter(own_fio, site): # returns Result string from ResultCluster
        my_scrapper = scrapper.Scrapper(Api.CHROME_DRIVER_DIR, own_fio, site) #be careful when putting fio data in 
        result_cluster = my_scrapper.execute()
        del my_scrapper
        return result_cluster.pretty_output()
    

    def contact_me():
        pass