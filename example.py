from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

ACCOUNT = '20513'
USERNAME = 'victor'
PASSWORD = 'Victor123'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://lite.serviceslogin.com/appointments.php?init=1")

wait = WebDriverWait(driver, timeout=120)

wait.until(
    EC.presence_of_element_located(
        (By.NAME, "_submit")
    )
)

account = driver.find_element(By.NAME, '_account')
account.send_keys(ACCOUNT)
username = driver.find_element(By.NAME, '_username')
username.send_keys(USERNAME)
password = driver.find_element(By.NAME, '_password')
password.send_keys(PASSWORD)
submit = driver.find_element(By.NAME, '_submit')
submit.click()

wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[@id='appt-menu-board']/a")
    )
)

driver.find_element(By.XPATH, "//*[@id='appt-menu-board']/a").click()

wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@id="frmFilter"]/div[4]/button')
    )
)

driver.find_element(By.XPATH, '//*[@id="frmFilter"]/div[4]/button').click()

wait.until(
    EC.element_to_be_clickable(
        (By.ID, 'btnSearch')
    )
)

Select(driver.find_element(By.ID, 'ddTimeRange')).\
    select_by_visible_text('This Week')
Select(driver.find_element(By.ID, 'ddStatus')).\
    select_by_visible_text('CLOSED')

# driver.find_element(By.ID, 'date_from').send_keys('2022-04-18')
# driver.find_element(By.ID, 'date_to').send_keys('2022-04-19')
driver.find_element(By.ID, 'btnSearch').click()

wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@data-status="CLOSED"]/tbody[1]')
    )
)

jobs = driver.find_elements(By.XPATH, '//*[@data-status="CLOSED"]/tbody[1]/tr')
print(len(jobs))
id_list = []
for job in jobs:
    id = job.get_attribute("id")
    id_list.append(id.split('-')[1])
job_info_list = []
# Open a new window
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
for id in id_list:
    new_url = 'https://lite.serviceslogin.com/addjob.php?board=1&jid=' + id
    driver.get(new_url)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="addjob-menu-comments"]/a')
        )
    )
    tech_name = Select(driver.find_element(By.ID, 'ddTech')).\
        first_selected_option.text
    job_info = {
        'id': id,
        'tech_name': tech_name,
    }
    job_info_list.append(job_info)
    print(job_info)
#print(job_info_list)
time.sleep(120)


driver.quit()
