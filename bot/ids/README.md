IDS is the Instrument Definition Service.

The goal of this service is to keep track of all avaliable assets in a file.
Assets can then be configured to whether or not they should be traded.

Design:
 - Polymarket Market Reader -> Grabs all markets from Polymarket
 - Market Selector -> Selects markets that should be tradable based on criteria
 - IDS Writing Client -> Writes the selected markets to a file

 
 - IDS Reading Client -> Reads the selected markets from a file (Used by the trading bot)