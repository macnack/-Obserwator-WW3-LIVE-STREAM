#!/usr/bin/env python3
import time
import wykop  # pip install wykop-sdk-reborn
import sys

klucz = "TWOJ KLUCZ"
sekret = "TWOJ SEKRET"

api = wykop.WykopAPI(klucz, sekret)

dlugosc_ramki = 80
def update_data():
    r = []
    for p in range(1, 50):
        sys.stderr.write('{:d}..\r'.format(p))
        r += api.tag('ukraina', page=p)
    return r

def naglowek(r,dlugosc, votes):
    lst = [(l['link']['date'], l['link']['title']) \
        for l in list(filter(lambda x: \
                                    x['type'] == 'link' and x['link']['vote_count'] >= votes, r))]
    lst = lst[0:dlugosc]
    return lst

def godzina_tekst(lst):
    out = []
    for d, t in lst:
        out.append('%s %s' % (d[11:-3] if d[11] != '0' else d[12:-3], t.replace('&quot;', '"')))
    return out
def tekst(lst):
    out = []
    for d, t in lst:
        out.append(t.replace('&quot;', '"'))
    return out

def main():
    r = update_data()
    lst = naglowek(r, 50, 100)
    pilne = godzina_tekst(lst)
    lst5 = naglowek(r, 10, 1000)
    uwaga = tekst(lst5)
    with open('./templates/template.html', 'r') as f:
        tpl = f.read()
        out = tpl.replace('{{NEWS}}', ' | '.join(pilne))
        with open('./output_files/pilne.html', 'w', encoding="utf_7") as f: f.write(out)

    with open('./templates/template2.html', 'r') as f:
        out = f.read()
        for idx in range(len(uwaga)):
            zamiennik = '{{NEWS' + str(idx) + '}}'
            if len(uwaga[idx]) > dlugosc_ramki:
                uwaga[idx] = uwaga[idx][:dlugosc_ramki] + '</span><span>' + uwaga[idx][dlugosc_ramki:]
        out = out.replace('{{NEWS}}', '</span><span>'.join(uwaga))
        with open('./output_files/PASEK_POLISH.html', 'w', encoding="utf_7") as f: f.write(out)

main()
while True:
    time.sleep(1800)
    main()
