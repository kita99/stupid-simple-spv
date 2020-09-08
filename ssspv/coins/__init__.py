from ssspv.settings import logging


# I'm a class, I swear
def Coin(currency_code):
    try:
        mod = __import__(f'ssspv.coins.{currency_code.lower()}', fromlist=[''])
    except Exception as e:
        logging.fatal(e)
        raise Exception(f'The coin {currency_code.upper()} is not implemented yet.')

    return getattr(mod, currency_code.upper())
