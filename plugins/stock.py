import json, urllib2
from util import hook, http

@hook.command
def stock(inp):
    '''.stock <symbol> -- gets stock information'''

    symbols = inp.split(',')
    # who needs more than 3 symbols
    url = ('http://finance.google.com/finance/info?client=ig&q=%s' % ','.join(symbols[:3]))
    
    try:
        raw = http.get(url)
    except urllib2.HTTPError as err:
        if err.code == 400:
            return "unknown ticker symbol %s" % inp
        else:
            return "error %s while retrieving data" % err.code
        
    # remove the comment stuff
    fixed = raw.replace('//', '')
    parsed = json.loads(fixed)
    
    s = []
    for q in parsed:
        quote = parsed[0]
        change = float(q['c'])
        
        quote['Name'] = q['t']
        quote['ChangePercentage'] = q['cp']
        quote['LastTradePriceOnly'] = "%.2f" % float(q['l'])
        quote['Change'] = ("+%.2f" % change) if change >= 0 else change

        if change < 0:
            quote['color'] = "5"
        else:
            quote['color'] = "3"   

        ret = "%(Name)s - %(LastTradePriceOnly)s \x03%(color)s%(Change)s (%(ChangePercentage)s%%)\x03" % quote
        s.append(ret)

    return ', '.join(s)
