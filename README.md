# Price Arbitrage

This is a program that alerts you when a specified item on ebay is significantly lower than the average listed price. It works by scanning through the ebay listings once to find the average price of the item, then scanning the listings on specific intervals afterwards to find items that are priced significantly lower than the average price. If items are found, a bot on discord will notify the user on the specified discord channel.

How to set up the program:<br>
        1. Set URL in application.py.<br>
        2. Set keywords to be excluded in application.py.<br>
        3. Set discord channel in application.py.<br>
        4. Set Discord token in application.py.<br>

How to use:<br>
        1. Run main.py.<br>
