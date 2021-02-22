import json, time
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome Dev\Application\chrome.exe"
options.add_argument("user-data-dir=C:\\Users\\newGen\\AppData\\Local\\Google\\Chrome Dev\\User Data")
driver = webdriver.Chrome(chrome_options = options, executable_path=r'chromedriver.exe')

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader, comment_start_string=r"{{#", comment_end_string=r"#}}")
template = env.get_template('email_format.html')

compose_p = '//div[text()="Compose"]'
to_p = '//textarea[@aria-label="To" or @name="to"]'
sub_p = '//input[@name="subjectbox" or @name="subjectbox" or @placeholder="Subject"]'
body_p = '//div[@aria-label="Message Body"]'
send_p = '//div[text()="Send"]'
msg_send_sign_p = '//span[text()="Message sent."]'

def findopj(pattern:str, delay:int = 10):
    try:
        return WebDriverWait(driver, delay).until(
            EC.visibility_of_element_located((By.XPATH, pattern))
        )
    except TimeoutException:
        return False

def entertext(text:str, pattern:str):
    opj = findopj(pattern)
    if opj:
        opj.send_keys(text)
    return opj

def send_mail(to:str, sub:str, mbody:str):
    opj0 = findopj(compose_p)
    if opj0:
        opj0.click()
        if entertext(to, to_p):
            if entertext(sub, sub_p):
                opj3 = findopj(body_p)
                if opj3:
                    driver.execute_script(fr"arguments[0].innerHTML = arguments[1];", opj3, mbody)
                    opj1 = findopj(send_p)
                    if opj1:
                        opj1.click()
                        opj2 = findopj(msg_send_sign_p, delay=15)
                        if opj2:
                            return True
    else:
        return False

def html_tem(data):
    return template.render(
        full_name=f"{data['first_name']} {data['last_name']}",
        user=data['username'],
        password=data['password'])

driver.get('https://mail.google.com/mail/u/0/#inbox')

subject = "Registration Confirmation from iskool71.com"

with open("employee_list.json", "r") as read_file:data = json.load(read_file)
for p in data:
    to_t = p["email"]
    if send_mail(
        to=to_t, 
        sub=subject, 
        mbody=html_tem(p)):
        print(f"Send successful! {p['email']}")
    else:
        raise(f"Error {p['email']}")
    time.sleep(1)
# driver.quit()