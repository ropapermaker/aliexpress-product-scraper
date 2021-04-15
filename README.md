# Aliexpress Product Scraper
Python script that scrapes products on aliexpress with selenium

## Usage
* You can change the link in `myUrl` variable of a page with products shown as a list.
* To change the number of pages scraped edit `for page_nb in range(1, 4)`
* Output goes to output.json or other specified name
* Information scraped:
  * title
  * store
  * price
  * review score
  * title
  * number sold
  * image link
  * product link
  * specifications of each product
* Sample included in this repo
