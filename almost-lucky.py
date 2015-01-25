#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import sys

def report_luckiness(receipt_serials, hit_serials):
    luckiness = {}

    for receipt in receipt_serials:
        data = {
            'hamming': [],
            'value': [],
            'triple_hit': False,
        }
        receipt_vector = map(int, receipt)
        for hit in hit_serials:
            # Hit!
            if receipt == hit:
                data['triple_hit'] = hit
                continue
            # Near
            value_distance = abs(int(receipt) - int(hit))
            if value_distance < 10:
                data['value'].append((hit, value_distance))
            # Digit hit
            hit_vector = map(int, hit)
            distance_vector = map(lambda r,h: abs(r-h), receipt_vector, hit_vector)
            matches = [ d==0 for d in distance_vector]
            if any(matches):
                data['hamming'].append((hit, matches.count(True)))
        print(receipt + ':', end='')
        if not any(data.values()):
            print('什麼都沒有:(')
        else:
            if data['triple_hit']:
                print('\033[32;1m' + hit, '三碼皆中，請檢查是否中獎！')
            if data['hamming']:
                for key, value in data['hamming']:
                    print('\033[33;1m{0}\033[0m(\033[31;1m{1}\033[0m碼相同)'.format(key, value), end='')
            if data['value']:
                for key, value in data['value']:
                    print('\033[33;1m{0}\033[0m(只差\033[31;1m{1}\033[0m碼)'.format(key, value), end='')
            print()
        luckiness[receipt] = data

    print('=====================================')
    print('全部', len(luckiness), '張')
    print('三碼皆中：', len(filter(lambda d: d['triple_hit'], luckiness.values())))
    print('兩碼次數：', sum( 1 for d in luckiness.values() for h in d['hamming'] if h[1] == 2))
    print('一碼次數：', sum( 1 for d in luckiness.values() for h in d['hamming'] if h[1] == 1))

    for distance in range(1, 10):
        number = sum( 1 for d in luckiness.values() for h in d['value'] if h[1] == distance)
        if not number: continue
        print('只差' + str(distance) + '碼：', number)

if __name__ == "__main__":

    try:
        receipt_serials = open(sys.argv[1], 'r').read().strip().splitlines()
        hit_serials = open(sys.argv[2], 'r').read().strip().splitlines()
    except:
        exit('./almost-lucky.py RECEIPT_SERIALS HIT_SERIALS')

    report_luckiness(receipt_serials, hit_serials)

