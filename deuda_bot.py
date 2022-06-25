#!/usr/bin/python3.8
#coding=utf-8

import time
import json
import random

from datetime import datetime
from keys import *

# NOTE: I put my keys in the keys.py to separate them from this main file.

#--------------------------------------------------------------------#
#                           FUNCTIONS                                #
#--------------------------------------------------------------------#

def generar_texto(i):
    data    = consultar_deuda(URL)
    ofi, real, pib, ofi_rel, real_rel, ofi_hab      = data[0], data[1], data[2], data[3], data[4], data[5]
    real_hab, km_autop, univesit, pernoc, hubble    = data[6], data[7], data[8], data[9], data[10] 
    base    = 'La deuda pública 🇪🇸 '
    text    = ['Actualización diaria de la deuda pública 🇪🇸:\n\nPIB: ' + pib + ' €/año.\n'
                + 'Deuda oficial: ' + ofi + '€ (' + "%.2f" % ofi_rel + '%)\nDeuda real: '
                + real + '€ (' + "%.2f" % real_rel + '%)',
                base + 'individual:\n\nOficial por habitante: ' + ofi_hab + '€\nReal por habitante: ' + real_hab + '€',
                base + 'equivale a ' + km_autop     + 'km de autopista (6.200.000€/km).',
                base + 'equivale a ' + univesit     + ' carreras universitarias (64.000€/carrera)',
                base + 'equivale a ' + pernoc       + ' pernoctaciones hospitalarias (955€/pernoctación).',
                base + 'equivale a ' + hubble       + ' telescopios HUBBLE (2.249.000.000€/unidad).']
    return text[i]

def consultar_deuda(URL):
    #deuda_ofi, deuda_real, PIB, ofi_hab, real_hab, km_autop, univesit, pernoc, hubble = get_data(URL)
    driver      = webdriver.Chrome(ChromeDriverManager().install())
    try:  
        driver      .get(URL)
        deuda_ofi   = driver.find_element_by_id('contador_PDET')
        deuda_real  = driver.find_element_by_id('contador_DRT')
        PIB         = driver.find_element_by_id('valor_costePIB')
        ofi_hab     = driver.find_element_by_id('contador_PDEH')
        real_hab    = driver.find_element_by_id('contador_PDEC')
        km_autop    = driver.find_element_by_id('contador_PDEC')
        univesit    = driver.find_element_by_id('contador_CUN')
        pernoc      = driver.find_element_by_id('contador_PHO')
        hubble      = driver.find_element_by_id('contador_HST')
        ofi         = deuda_ofi .text
        real        = deuda_real.text
        pib         = PIB.text
        ofi_rel     = int(ofi   .replace('.', ''))/int(pib  .replace('.', ''))*100
        real_rel    = int(real  .replace('.', ''))/int(pib  .replace('.', ''))*100
        data        = [ofi, real, pib, ofi_rel, real_rel, ofi_hab.text, real_hab.text, km_autop.text, univesit.text, pernoc.text, hubble.text]

    finally:
        driver.quit()

    return      data

def tweet(text, user_id):
    obj_now = datetime.now()
    print('Tweeting:\n------------------------------------\n' + text)
    print("Current date & time: ", obj_now)
    print('------------------------------------')
    if (user_id):
        api.update_status(text, user_id)
    else:
        api.update_status(text)

def retrieve_last_seen_id(file_name):
    f_read          = open(file_name, 'r')
    last_seen_id    = int(f_read.read().strip())
    f_read          .close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write .write(str(last_seen_id))
    f_write .close()

def reply_to_tweets():
    global ADJETIVOS, SUSTANTIVOS
    last_seen_id    = retrieve_last_seen_id(FILE_NAME)      # First id mention was 1351237398852726786
    mentions        = api.mentions_timeline(last_seen_id, tweet_mode = 'extended')

    for mention in reversed(mentions):
        time.sleep(5)
        print('--------------------------------', flush=True)
        print('Found mention:'                  , flush=True)

        print(str(mention.id) + '(@' + mention.user.screen_name + ') - ' + mention.full_text, flush=True)
        last_seen_id            = mention.id
        store_last_seen_id      (last_seen_id, FILE_NAME)
        word_1  = SUSTANTIVOS   [random.randrange(len(SUSTANTIVOS))]
        word_2  = ADJETIVOS     [random.randrange(len(ADJETIVOS))]
        
        if '#insultame' in mention.full_text:
            answer = '@' + mention.user.screen_name + ' ' + word_1 + ' ' + word_2 # + ' te insulto'
            print('Found #insultame! Responding back...')
            tweet(answer, mention.id)

        if '#deuda' in mention.full_text:
            data    = consultar_deuda(URL)
            ofi, ofi_rel, real, real_rel = data[0], data[3], data[1], data[4]
            answer = '@' + mention.user.screen_name + ' Aquí tienes 🇪🇸:\n\nDeuda oficial: ' + ofi + '€ (' + "%.2f" % ofi_rel + '%)\nDeuda real: ' + real + '€ (' + "%.2f" % real_rel + '%)'
            print('Found #deuda! Responding back...')
            tweet(answer, mention.id)

#--------------------------------------------------------------------#
#                           MAIN LOOP                                #
#--------------------------------------------------------------------#

i = 0
j = 1440 # 2h gap

while 1:
    reply_to_tweets()
    time.sleep(5)
# while 1:
#     # TWEET DEBT
#     if i % 17280 == 0: # 86400 secs / 5 secs per iteration
#         tweet(generar_texto(0), False)

#     # TWEET RANDOM FACT
#     if j % 17280 == 0:
#         tweet(generar_texto(random.randrange(1, 6)), False)

#     reply_to_tweets()
#     time.sleep(5)
#     i += 1
#     j += 1
