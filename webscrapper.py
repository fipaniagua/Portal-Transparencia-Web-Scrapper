from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep
from openpyxl import Workbook, load_workbook

def clean_extra_tabs():
    handles = browser.window_handles
    for i in range(len(handles)):
            if i != 0:
                browser.switch_to_window(handles[i])
                browser.close()
    browser.switch_to_window(handles[0])

def save_meta_data(org, sub_org, tipo_contrato, mes, year, website, extra = None, second_colum = ""):
    wb = load_workbook('./links_muni/datos_links_{0}.xlsx'.format(second_colum))
    ws = wb.active
    ws.append([org, sub_org, tipo_contrato, mes, year, extra, website])
    wb.save('./links_muni/datos_links_{0}.xlsx'.format(second_colum))
    return


def get_options_by_class(class_name):
    browser.implicitly_wait(4)
    sub_contents = browser.find_elements_by_class_name(class_name)
    sub_options = []
    for sub_content in sub_contents:
        sub_options.append(sub_content.get_attribute("id"))
    return sub_options



def handler_second_window_1(org, sub_org, windows_3 = False, sub_option=""):
    differents = ["Política de Remuneraciones del Consejo para la Transparencia",
                  "Histórico de Personal y Remuneraciones a Diciembre 2013",
                  "Escala Remuneraciones (*)", "Escala Remuneraciones" ]
    browser.switch_to_window(browser.window_handles[1])
    amount_contracts = len(browser.find_elements_by_xpath('//*[@id="A2248:form:j_idt30:0:datalist_list"]/li[4]//a'))
    for index_contract in range(amount_contracts):
        contract = browser.find_elements_by_xpath('//*[@id="A2248:form:j_idt30:0:datalist_list"]/li[4]//a')[index_contract]
        if not contract.get_attribute("title") in differents:
            tipo_contrato = contract.get_attribute("title")
            print(tipo_contrato)
            contract.click()
            browser.implicitly_wait(0)
            conteiner = browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]')
            browser.implicitly_wait(4)
            if len(conteiner) > 0:
                amount_anos = len(browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a'))
                #anos_ids = [ano_link.get_attribute("id") for ano_link in anos_links]

                for index_ano in range(amount_anos):
                    ano_link = browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a')[index_ano]
                    ano_text = ano_link.text
                    ano_link.click()
                    amount_meses = len(browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a'))
                    for index_mes in range(amount_meses):
                        mes_link = browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a')[index_mes]
                        mes_text = mes_link.text
                        mes_link.click()
                        if windows_3:
                            amount_links = len(browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a'))
                            for index_link in range(amount_links):
                                link = browser.find_elements_by_xpath('//*[@id="A2248:form-visualizar:preview-tipo-padre"]//a')[index_link]
                                link_text = link.text
                                link_href = link.get_attribute('href')
                                #link.click()
                                save_meta_data(org, sub_org, tipo_contrato, mes_text, link_text, link_href, ano_text, sub_option)
                        else:
                            save_meta_data(org, sub_org, tipo_contrato, ano_text, mes_text, link_href, sub_option)
                        sleep(1)
                        browser.back()
                    browser.back()

            sleep(1)
            browser.back()
    browser.close()
    browser.switch_to_window(browser.window_handles[0])
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

start = False
org_with_3options = [0,11,12]
sub_org_with_3options = ["Corporaciones Municipales"]
i = 12
for id_option in options[12:13]:
    print("scope1:", id_option, "i:", i)
    try:
        browser.get(page_url)
        org = browser.find_element_by_id(id_option).text
        browser.find_element_by_id(id_option).click()
    except Exception as e1:
        browser.get(page_url)
        org = browser.find_element_by_id(id_option).text
        browser.find_element_by_id(id_option).click()

    if i in org_with_3options :


        sub_options = get_options_by_class('dor_org_hijo_no_senialado')
        for sub_option in sub_options:
            print("scope2:", sub_option)
            try:
                browser.implicitly_wait(5)
                sub_org = browser.find_element_by_id(sub_option).text
                browser.find_element_by_id(sub_option).click()
            except Exception as e2:
                browser.implicitly_wait(5)
                sub_org = browser.find_element_by_id(sub_option).text
                browser.find_element_by_id(sub_option).click()
            sleep(1)
            amount_links = len(browser.find_elements_by_xpath('//*[@id="A3684:form:organismos"]//a'))
            print(amount_links)
            for index_link in range(amount_links):
                link = browser.find_elements_by_xpath('//*[@id="A3684:form:organismos"]//a')[index_link]
                sub_org_name = link.text
                print("*",sub_org_name)

                if sub_org_name in "Municipalidad de Algarrobo":
                    start = True
                if not start:
                    continue
                if sub_org_name in "Municipalidad de Zapallar":
                    raise Exception


                link.click()
                browser.implicitly_wait(15)
                btn_to_new_window = browser.find_element_by_partial_link_text('Vea la informac')
                browser.implicitly_wait(5)
                if "portaltransparencia" in btn_to_new_window.get_attribute("href"):
                    if sub_org in sub_org_with_3options:
                        windows_3 = True
                    else:
                        windows_3 = False
                    windows_3 = True
                    clean_extra_tabs()
                    btn_to_new_window.click()
                    handler_second_window_1(org, sub_org_name, windows_3, sub_org)
                sleep(1)
                try:
                    browser.get(page_url)
                    browser.find_element_by_id(id_option).click()
                    browser.find_element_by_id(sub_option).click()
                except Exception as e3:
                    browser.get(page_url)
                    browser.find_element_by_id(id_option).click()
                    browser.find_element_by_id(sub_option).click()
                sleep(1)


    elif i != 4:
        browser.implicitly_wait(5)
        sub_contents = browser.find_elements_by_xpath("//*[@class='dor_organismos_selecc Class_id_link_org_link']")
        sub_options = [sub_content.get_attribute("id") for sub_content in sub_contents]
        print(len(sub_options))
        for sub_option in sub_options:
            print(sub_option)
            sub_org = browser.find_element_by_id(sub_option).text
            browser.find_element_by_id(sub_option).click()
            btn_to_new_window = browser.find_element_by_partial_link_text('Vea la informac')
            if "portaltransparencia" in btn_to_new_window.get_attribute("href"):
                btn_to_new_window.click()
                handler_second_window_1(org, sub_org)
            sleep(1)
            try:
                browser.get(page_url)
                browser.find_element_by_id(id_option).click()
            except Exception as e3:
                browser.get(page_url)
                browser.find_element_by_id(id_option).click()

    i += 1
    sleep(1)
