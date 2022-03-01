import tweepy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#--------------------------------------------------------------------#
#                           TWITTER CONSTANTS                        #
#--------------------------------------------------------------------#

# your developer twitter keys here
CONSUMER_KEY    = ''
CONSUMER_SECRET = ''
ACCESS_KEY      = ''
ACCESS_SECRET   = ''

auth        = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth        .set_access_token(ACCESS_KEY, ACCESS_SECRET)
api         = tweepy.API(auth, wait_on_rate_limit = True)

FILE_NAME   = 'last_seen_id.txt'

#--------------------------------------------------------------------#
#                           CHROME CONSTANTS                         #
#--------------------------------------------------------------------#

# PATH        = './chromedriver.exe'
URL         = 'https://deuda-publica-espana.com/'
# driver      = webdriver.Chrome(PATH)

#--------------------------------------------------------------------#
#                           INSULTOS                                 #
#--------------------------------------------------------------------#

ADJETIVOS   = ['sinvergüencilla', 'apaleado', 'mancillado', 'maleante', 'mediocre', 'charlatán', 'analfabeto', 'canalla', 'canallica',
                'cobarde', 'chupasangre', 'zampabollos', 'mellado', 'chupasangre', 'Bellaco', 'Bebecharcos', 'Bocachancla', 'Chupacables',
                'Chupóptero', 'Comeflores', 'Culopollo', 'Escornacabras', 'Malparido', 'chiflado']
SUSTANTIVOS = ['Granjero', 'Payaso', 'Cuerpo escombro', 'Lastre', 'Adoquín', 'Mantecado', 'Piltrafilla', 'Granuja',
                'Canalla', 'Canallica', 'Zapato', 'Camello', 'Dromedario', 'Higo', 'Avestruz', 'Alcornoque', 'Alfeñique', 'Cabestro',
                'Cabezabuque', 'Calientahielos', 'Caracartón', 'Caraflema', 'Zoquete', 'Berberecho']
