from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def get_options_by_class(class_name):
    browser.implicitly_wait(40)
    sub_contents = browser.find_elements_by_class_name(class_name)
    sub_options = []
    for sub_content in sub_contents:
        sub_options.append(sub_content.get_attribute("id"))
    return sub_options


def handler_second_window_1():
    differents = ["Política de Remuneraciones del Consejo para la Transparencia Enlace Externo",
                  "Histórico de Personal y Remuneraciones a Diciembre 2013 ",
                  "Escala Remuneraciones (*)" ]
    browser.switch_to_window(browser.window_handles[1])
    contracts_links = browser.find_elements_by_xpath('//*[@id="A2248:form:j_idt30:0:datalist_list"]/li[4]//a')
    contracts_ids = [contract.get_attribute("id") for contract in contracts_links]
    for contract_id in contracts_ids:
        contract = browser.find_element_by_id(contract_id)
        if not contract.get_attribute("title") in differents:
            print(contract.get_attribute("title"))
            contract.click()
            browser.implicitly_wait(0)
            conteiner = browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]')
            browser.implicitly_wait(40)
            if len(conteiner) > 0:
                amount_anos = len(browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a'))
                #anos_ids = [ano_link.get_attribute("id") for ano_link in anos_links]

                for index_ano in range(amount_anos):
                    ano_link = browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a')[index_ano]
                    ano_link.click()
                    amount_meses = len(browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a'))
                    for index_mes in range(amount_meses):
                        mes_link = browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a')[index_mes]
                        mes_link.click()
                        sleep(1)
                        browser.back()

                    browser.back()

            sleep(2)
            browser.back()

    sleep(5)
    browser.close()
    browser.switch_to_window(browser.window_handles[0])
    sleep(5)
    return

path_to_chromedriver = "./chromedriver"
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
main_page_url = "https://www.portaltransparencia.cl/PortalPdT/web/guest/home"
page_url = "https://www.portaltransparencia.cl/PortalPdT/web/guest/directorio-de-organismos-regulados"

browser.get(main_page_url)
first_link_xpath = "/html/body/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/div[1]/a[2]"
browser.find_element_by_xpath(first_link_xpath).click()

contents = browser.find_elements_by_class_name('dor_org_no_senialado')
options = [content.get_attribute("id") for content in contents]

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
                browser.implicitly_wait(40)
                browser.find_element_by_id(sub_option).click()
            except Exception as e2:
                browser.find_element_by_id(sub_option).click()
    elif i != 4:
        sub_contents = browser.find_elements_by_xpath("//*[@class='dor_organismos_selecc Class_id_link_org_link']")
        sub_options = [sub_content.get_attribute("id") for sub_content in sub_contents]
        for sub_option in sub_options:
            print(sub_option)
            browser.find_element_by_id(sub_option).click()
            btn_to_new_window = browser.find_element_by_partial_link_text('Vea la informac')
            if "portaltransparencia" in btn_to_new_window.get_attribute("href"):
                btn_to_new_window.click()
                handler_second_window_1()
            sleep(2)
            try:
                browser.get(page_url)
                browser.find_element_by_id(id_option).click()
            except Exception as e3:
                browser.get(page_url)
                browser.find_element_by_id(id_option).click()

    i += 1
    sleep(1)
