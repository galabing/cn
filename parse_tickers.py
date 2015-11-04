#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import codecs
import re

# Eg, <li><a target="_blank" href="http://quote.eastmoney.com/sz500159.html">景顺500(500159)</a></li>
PATTERN = ('^<li><a target="_blank" href="http://quote.eastmoney.com/'
           '(?P<exchange>sh|sz)(?P<ticker1>\d+).html">(?P<name>.+)\((?P<ticker2>\d+)\)</a></li>$')
PROG = re.compile(PATTERN, re.UNICODE)

def get_category(name):
  if name.endswith('B') or name.endswith('B股'):
    return 'B'
  return 'A'

def parse_tickers(input_file, output_file):
  with codecs.open(input_file, 'r') as fp:
    lines = [line.strip() for line in fp.read().splitlines()]
  tickers = dict()  # ticker => name, exchange, A/B
  for line in lines:
    m = PROG.match(line)
    if m is None: continue
    exchange = m.group('exchange')
    ticker1 = m.group('ticker1')
    ticker2 = m.group('ticker2')
    name = m.group('name')
    assert ticker1 == ticker2, 'inconsistent tickers: %s vs %s' % (ticker1, ticker2)
    assert ticker1 not in tickers, 'dup tickers: %s' % ticker1
    tickers[ticker1] = [name, exchange, get_category(name)]
  with codecs.open(output_file, 'w') as fp:
    for ticker in sorted(tickers.keys()):
      name, exchange, category = tickers[ticker]
      fp.write(ticker + '\t' + name + '\t' + exchange + '\t' + category + '\n')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input', required=True)
  parser.add_argument('--output', required=True)
  args = parser.parse_args()
  parse_tickers(args.input, args.output)

if __name__ == '__main__':
  main()
