from threading import local
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
import config
import time
import localization

xpath = '//*[@id="offer-requests-body"]/div[contains(@class,"offer-request request-status-")]'
xpath_n = xpath + '/div[@class="offer-request-n"]' + '/div'
xpath_fio = xpath + '/div[@class="offer-request-fio"]' + '/div'
xpath_status = xpath + '/div[@class="offer-request-status"]' + '/div'
xpath_priority = xpath + '/div[@class="offer-request-priority"]' + '/div'



class Scrapper():

    MAX_BUTTON_APPEARENCE = 5
    MAX_LATENCY = 1.5
    LAST_LATENCY = 5

    person = {
        "fio":None,
        "status":None,
        "priority":None
    }

    status_ACCEPTED = "рекомендовано (бюджет)"
    status_ABLE = "допущено"
    status_ORDERED = "до наказу (бюджет)"


    def __init__(self, chrome_driver_dir, fio, primary_table_website):
        #hiding the browser
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
        self.driver = webdriver.Chrome(chrome_driver_dir, chrome_options=options)
        self.fio = fio
        self.n = 0
        self.members_to_compare = 0
        self.excluded_members = 0
        self.primary_website = primary_table_website
        self.included_websites = self._get_websites(self.primary_website)
        self.result_init_data = []


    def _get_websites(self, exclude):
        websites = []
        for college in config.tables:
            for site in config.tables[college]:
                if site != exclude:
                    websites.append(site)
                else:
                    continue
        return websites


    def get_actual_n(self):
        return self.n - self.excluded_members


    def get_members_by_priority_in_primary(self, priority="К"):
        self._connect_to_website(self.primary_website)
        member_count = len(self.driver.find_elements_by_xpath(xpath))
        self.result_init_data.append(member_count) #total_number
        members = []
        STT = time.time()##
        parsed_fio = self.driver.find_elements_by_xpath(xpath_fio)
        print(len(parsed_fio))
        parsed_status = self.driver.find_elements_by_xpath(xpath_status)
        parserd_priority = self.driver.find_elements_by_xpath(xpath_priority)
        print(time.time() - STT)##
        STT = time.time() ##
        for i in range(member_count):
            fio = parsed_fio[i].text
            if fio == self.fio:
                print("NNNNNNNNNN")
                self.n = len(parsed_fio[:i])
                break
            else:
                status = parsed_status[i].text
                _priority = parserd_priority[i].text
                if status == Scrapper.status_ABLE and _priority == priority:
                    #print(f'ФИО: {local_member["fio"]}| Статус: {local_member["status"]}| Приоритет: {local_member["priority"]}| Балл: {local_member["mark"]};')
                    members.append(fio)

            
        self.result_init_data.append(len(members)) #before me
        print(time.time() - STT)##
        self.members_to_compare = members
        
        return members


    def compare(self):
        STT = time.time()
        members_to_exclude = 0
        for website in self.included_websites:
            if not self.members_to_compare:
                break
            self._connect_to_website(website)
            parsed_fio = self.driver.find_elements_by_xpath(xpath_fio)
            parsed_status = self.driver.find_elements_by_xpath(xpath_status)
            members_count = len(parsed_fio)
            print("site connection iteration")

            for i in range(members_count):
                status = parsed_status[i].text
                if status == Scrapper.status_ACCEPTED:
                    fio = parsed_fio[i].text
                    if fio in self.members_to_compare:
                        members_to_exclude += 1
                        self.members_to_compare.pop(self.members_to_compare.index(fio))
                        print("add")
                elif status == Scrapper.status_ORDERED:
                    continue
                else:
                    break
        self.excluded_members = members_to_exclude

        print(time.time() - STT)
        return members_to_exclude
        
            
    def _connect_to_website(self, website):
        self.driver.get(website) #121 for exemple
        for attempt in range(Scrapper.MAX_BUTTON_APPEARENCE):
            try:
                button = self.driver.find_element_by_id("requests-load")
                button.click()
                if attempt != 4:
                    time.sleep(Scrapper.MAX_LATENCY)
                else: 
                    time.sleep(Scrapper.LAST_LATENCY) #Waiting for table finally load -> after the 5th button click the site loads the remains
                print("looping")##
            except:
                break
        print("finished looping")##


    def execute(self): #website -> config 
        self.result_init_data = [] #overriding
        self.get_members_by_priority_in_primary()
        self.compare()
        self.result_init_data.append(self.n) #unfiltered place
        self.result_init_data.append(self.excluded_members) #legitemately excluded
        actual_n = self.get_actual_n()
        self.result_init_data.append(actual_n) #filtered place

        return ResultCluster(*self.result_init_data)


class ResultCluster():
    def __init__(self, total_number, to_excluide_before_me, unfiltered_pos, legit_excluded_before_me, filtered_pos):
        self.total_number = total_number
        self.to_exclude = to_excluide_before_me
        self.excluded = legit_excluded_before_me
        self.unfiltered_pos = unfiltered_pos
        self.filtered_pos = filtered_pos

    
    def pretty_output(self):
        return f'''{localization.ResultCluster.RU.total_number} {self.total_number}
        {localization.ResultCluster.RU.to_exclude} {self.to_exclude}
        {localization.ResultCluster.RU.excluded} {self.excluded}
        {localization.ResultCluster.RU.unfiltered_pos} {self.unfiltered_pos}
        {localization.ResultCluster.RU.filtered_pos} {self.filtered_pos}'''

#+1 погрешность