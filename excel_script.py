from openpyxl import Workbook, load_workbook


def save_meta_data(org, sub_org, tipo_contrato, mes, year, website):
    wb = load_workbook('datos_links.xlsx')
    ws = wb.active
    ws.append([org, sub_org, tipo_contrato, mes, year, website])
    wb.save('datos_links.xlsx')
    return



save_meta_data("a","b","c","d","e",3)
