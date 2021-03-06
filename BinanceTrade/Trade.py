from math import e
from binance.client import Client
from BinanceTrade.FutureTrade import *

try : 
    from config_dev import API_BINANCE_KEY , API_BINANCE_SECRET
except Exception:
    from config_prod import API_BINANCE_KEY , API_BINANCE_SECRET

# from DB.Firebasedb import GetDataBotsetting

client = Client( API_BINANCE_KEY , API_BINANCE_SECRET )

def ReceiveSignals(signal_data_dict):

    Signal_Type = signal_data_dict["ACTION"].split(" ")[0]
    Signal_Side = signal_data_dict["ACTION"].split(" ")[1]
    Signal_Lev = int(signal_data_dict["LEV"])
    Signal_Symbol = signal_data_dict["SYMBOL"]

    msg = ""

    #  USDT 
    amount = 50

    # CHECK WHICH SIDE TO CLOSE ?
    CLOSE_side = "LONG"
    if Signal_Side == "LONG":
        CLOSE_side = "SHORT"

    if Signal_Type == "OPEN":
        # Close before open
        try:
            ClosePositionAtMarket(symbol=Signal_Symbol, positionSide=CLOSE_side)
        except Exception as e:
            print(e)
            msg += str(e)
        # open pos (NOTPSL)
        try:
            PlaceOrderAtMarket(position=Signal_Side, symbol=Signal_Symbol, amount=amount, lev = Signal_Lev)
            msg = "ทำการ {} Position ในฝั่ง {} คู่สินค้า {} ".format(Signal_Type,Signal_Side,Signal_Symbol)
        except:
            msg += str(e)
        
    elif Signal_Type == "TPSL":
        # Close Position by the signal side ....
        try:
            ClosePositionAtMarket(symbol=Signal_Symbol, positionSide=Signal_Side)
            msg = "ทำการ {} Position ในฝั่ง {} คู่สินค้า {} ".format(Signal_Type,Signal_Side,Signal_Symbol)
        except Exception as e:
            msg += str(e)
    return msg