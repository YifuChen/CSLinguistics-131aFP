import re
from collections import defaultdict
from num2word import digit2word
from num2word import num2word


class CurrencyNormalizer:

    def __init__(self):
        self.abbreviationDict = defaultdict(list)
        self.abbreviationDict["usd"] = (["u.s. dollar", "cent"],
                                        ["u.s. dollars", "cents"])
        self.abbreviationDict["gbp"] = (["pound", "penny"],
                                        ["pounds", "pence"])
        self.abbreviationDict["eur"] = (["euro", "cent"],
                                        ["euros", "cents"])
        self.abbreviationDict["jpy"] = (["yen", "sen"],
                                        ["yens", "sens"])
        self.abbreviationDict["aud"] = (["australian dollar", "cent"],
                                        ["australian dollars", "cents"])
        self.abbreviationDict["cad"] = (["canadian dollar", "cent"],
                                        ["canadian dollars", "cents"])
        self.abbreviationDict["chf"] = (["swiss franc", "rappen"],
                                        ["swiss francs", "rappen"])
        self.abbreviationDict["sek"] = (["swedish krona", "ore"],
                                        ["swedish kronor", "ore"])
        self.abbreviationDict["hkd"] = (["hong kong dollar", "cent"],
                                        ["hong kong dollars", "cents"])

        self.symbolDict = defaultdict(list)
        self.symbolDict["$"] = (["dollar", "cent"],
                                ["dollars", "cents"])
        self.symbolDict["£"] = (["pound", "penny"],
                                ["pounds", "pennies"])
        self.symbolDict["€"] = (["euro", "cent"],
                                ["euros", "cents"])
        self.symbolDict["¥"] = (["yen", "sen"],
                                ["yens", "sens"])
        self.symbolDict["fr"] = (["swiss franc", "rappen"],
                                 ["swiss francs", "rappen"])
        self.symbolDict["fr."] = (["swiss franc", "rappen"],
                                  ["swiss francs", "rappen"])
        self.symbolDict["kr"] = (["swedish krona", "ore"],
                                 ["swedish kronor", "ore"])

        self.scaleDict = dict()
        self.scaleDict["million"] = "million"
        self.scaleDict["m"] = "million"
        self.scaleDict["mn"] = "million"
        self.scaleDict["billion"] = "billion"
        self.scaleDict["b"] = "billion"
        self.scaleDict["bn"] = "billion"
        self.scaleDict["trillion"] = "trillion"
        self.scaleDict["t"] = "trillion"
        self.scaleDict["tn"] = "trillion"

    """"normalize a tokenized currency input into english words
        currency tuple: (symbol/abbr, int, decimal, scale)"""
    def normalize_currency(self, input):

        try:
            input = input.groups('')
        except AttributeError:
            pass

        currency = input[0]
        num = input[1]
        decimal = input[2]
        scale = input[3]
        res = []

        # append non-decimal number and currency word
        res.extend([self.normalize_number(num),
                    self.get_currency_word(currency, num == '1')])

        # append scale if exist
        if scale != '':
            if decimal != '':
                res[len(res) - 1: len(res) - 1] = ['point', self.normalize_decimal(decimal)]
            res[len(res) - 1: len(res) - 1] = [self.get_scale_word(scale)]

        # append decimal number and currency word(if only 2 decimal)
        # append the "cents" equivalent currency word if the number has two
        # decimal place and no scale
        elif decimal != '':
            if len(decimal) == 2 and decimal != '00':
                cent_number = self.normalize_number(decimal)
                res.extend(['and', cent_number,
                            self.get_currency_word(currency, cent_number == 'one', True)])
            else:
                res[len(res) - 1: len(res) - 1] = ['point', self.normalize_decimal(decimal)]
        res.append('')
        return ' '.join(res)

    """get the currency's english word. If is_single is true return singular 
        form (ex: dollar). Otherwise return plural form (ex: dollars).
    """
    def get_currency_word(self, currency_token, is_single, has_cent=False):
        # currency_token is abbreviation
        if currency_token.lower() in self.abbreviationDict:
            if not has_cent:
                return self.abbreviationDict.get(currency_token)[0][0] if is_single else\
                       self.abbreviationDict.get(currency_token)[1][0]
            else:
                return self.abbreviationDict.get(currency_token)[0][1] if is_single else\
                       self.abbreviationDict.get(currency_token)[1][1]
        # currency_token is symbol
        elif currency_token.lower() in self.symbolDict:
            if not has_cent:
                return self.symbolDict.get(currency_token)[0][0] if is_single else\
                       self.symbolDict.get(currency_token)[1][0]
            else:
                return self.symbolDict.get(currency_token)[0][1] if is_single else\
                       self.symbolDict.get(currency_token)[1][1]

    def get_scale_word(self, scale_token):
        # currency_token is abbreviation
        return self.scaleDict.get(scale_token.lower())

    """normalize the numbers before the decimal points into english words using 
        num2words module. Whitespaces and non-digit char such as ',' are ignored
        ex: 1234 "one thousand, two hundred and thirty-four"
    """
    def normalize_number(self, number):
        return ' '.join(num2word(''.join(re.findall(r'\d', number))))

    """normalize the numbers after the decimal points into english words.
        ex: for 0.1234, the "1234" is passed as input and return "one two 
        three four"
    """
    def normalize_decimal(self, decimal):
        return ' '.join(digit2word(decimal))


if __name__ == '__main__':

    pass
