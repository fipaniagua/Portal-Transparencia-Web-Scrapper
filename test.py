from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def get_options_by_class(class_name):
    browser.implicitly_wait(40)
    #sub_contents = browser.find_elements_by_xpath("//*[@class='dor_organismos_selecc Class_id_link_org_link']")

    sub_contents = browser.find_elements_by_class_name(class_name)
    sub_options = []
    for sub_content in sub_contents:
        sub_options.append(sub_content.get_attribute("id"))


    return sub_options




path_to_chromedriver = "./chromedriver"
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
main_page_url = "https://www.portaltransparencia.cl/PortalPdT/web/guest/home"
page_url = "https://www.portaltransparencia.cl/PortalPdT/web/guest/directorio-de-organismos-regulados"

browser.get(main_page_url)
first_link_xpath = "/html/body/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/div[1]/a[2]"
browser.find_element_by_xpath(first_link_xpath).click()

contents = browser.find_elements_by_class_name('dor_org_no_senialado')
options = [content.get_attribute("id") for content in contents]

#<a href="#"  8 id="A3684:form:j_idt37:2:j_idt39" name="A3684:form:j_idt37:2:j_idt39" onclick="jsf.util.chain(this,event,&quot;funcionDisableLinkOrgType3();&quot;,&quot;RichFaces.ajax(\&quot;A3684:form:j_idt37:2:j_idt39\&quot;,event,{\&quot;incId\&quot;:\&quot;1\&quot;} )&quot;);return false;" class="dor_organismos_selecc Class_id_link_org_link">CFT de la Región de los Lagos</a>
org_with_3options = [0,11,12]
i = 0
for id_option in options[:18]:
    print("scope1:", id_option, "i:", i)
    try:
        browser.get(page_url)
        browser.find_element_by_id(id_option).click()
    except Exception as e1:
        browser.find_element_by_id(id_option).click()

    if i in org_with_3options :
        sub_options = get_options_by_class('dor_org_hijo_no_senialado')
        for sub_option in sub_options:
            print("scope2:", sub_option)
            try:
                browser.find_element_by_id(sub_option).click()
            except Exception as e2:
                browser.find_element_by_id(sub_option).click()


    i += 1
    sleep(1)
