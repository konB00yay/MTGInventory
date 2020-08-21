# MTGInventory
Inventory application as I try to sell all my MTG cards from when I was a kid

Initially developed as a web application using Django
run with: python manage.py runserver
and visit at http://127.0.0.1:8000/

# Inventory
The inventory page is the home page for the application, holding a table with all your card instances that are uploaded. In order to upload more cards to your collection
simply browse and select your card CSV file to upload. Upload only accepts CSV files in the following order: Name, Edition, Foil, Quantity, Bag
- Name - the name of the card being uploaded (replace all commas in the name with semicolons for correct parsing)
- Edition - edition of the card, edition abbreviations must be in line with https://mtg.gamepedia.com/Template:List_of_Magic_sets
- Foil - boolean on if the card is foil or not
- Quantity - how many cards to add to the collection
- Bag - location for where the card is in your collection. In the beginning I developed this while only uploading 100 cards at a time and organizing them into various bags of 100 cards. This ensures I know how many cards are in each bag and I can find them.

# Sell
The Sell page is a holding table for all the cards you have sold and how much you have earned per card sold. A running total of profit is listed above the table, where the sold cards are displayed.
In order to add to the sell table and update your profits simply browse for your sell CSV file and upload. Sell only accepts CSV files in the following order: Name, Edition, Foil, Quantity, Profit
- Name - the name of the card being uploaded (replace all commas in the name with semicolons for correct parsing)
- Edition - edition of the card, edition abbreviations must be in line with https://mtg.gamepedia.com/Template:List_of_Magic_sets
- Foil - boolean on if the card is foil or not
- Quantity - how many cards to add to the collection
- Profit - how much the total sell of the quantity of cards was for this spcific card

# Market
The Market page is the most interesting page and holds the most information. By selecting the 'Gather Market Data' button the application begins a web scraping process
using BeautifulSoup to find all of the cards being sold at CardKingdom. It then parses out the information such as the name, edition, foil, and market value and stores
in the MarketCard database. This way you do not need to gather market data every time you start up the application as it is a slow process. The 'Apply Data' button begins 
to go through the MarketCard database and cross reference cards in that DB and the cards in your inventory. When there is a match it determines how much value your inventory
of that card is worth. After all of the Market data has been analyzed the table on the Market page is updated to display the card in your inventory, the bag(s) it is in, and
the total value it is worth, including the quantity of that card.
