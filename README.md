# Portal Transparencia Web scrapper
I use **selenium** library to make a scrapper for http://portaltransparencia.cl/ chilean goberment page. Also use **beutifulsoup** + **openpyxl** to save web html tables into xlsx files.

## Usage

* Modify webscrapper.py to tune the needed parameters. (from *run* function) 
* Run webscrapper.py, this will save the links to the web tables, along side their respective metadata, in data_links.xlsx . 
* Run web_table_downloader.py, this will go through saved links and will parse the data from the web html tables into a .xlsx file in the data folder.

## Api

run(start ,end, org_with_3row ,sub_org_with_3options, org_with_3options,differents,  page_url)

Parameter | Description
----------- | -----------
Start | the index of the organization in wich you want to start to gather data
End | the index of the organization in witch you want to end of gather data
Org_with_3row | the name of the organizations with an extra row to select the sub organization
Sub_org_with_3options | the name of the sub organization wich have more than 3 links to get to the tables
Org_with_3options | the name of the organization wich have more than 3 links to get to the tables
Differents | the name of the contracts in wich won't be collected data
Page_url | the url of the page
