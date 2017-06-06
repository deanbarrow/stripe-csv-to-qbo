import csv
import argparse
import time
import math


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='+', type=argparse.FileType('r'))
    args = parser.parse_args()

    transactions = []
    for f in args.infile:
        for line in csv.DictReader(f):
            # The single line has a gross payment and a fee payment, so we need to split those apart
            tstamp = time.strptime('{Created (UTC)}'.format(**line), '%Y-%m-%d %H:%M')

            if line['Status'] != 'Failed':

                # This is the "gross" payment
                transactions.append((
                    tstamp,
                    'Stripe - {Status} {Description} From {Card Name} {Customer Email (metadata)}'.format(**line),
                    line['Amount'].replace(',', '')
                ))

                if line['Fee'] != '0.00':
                    transactions.append((
                        tstamp,
                        'Stripe - {Status} Fee {Description} From {Card Name} {Customer Email (metadata)}'.format(**line),
                        '-' + line['Fee'].replace(',', '')
                    ))

    for filenum in range(0, int(math.ceil(len(transactions) / 1000.0))):
        with open('StripeQuickBooksOutput%d.csv' % (filenum + 1), 'w') as f:
            i = 0
            writer = csv.DictWriter(f, fieldnames=['Date', 'Description', 'Amount'])
            writer.writeheader()

            for txn in sorted(transactions, key=lambda l: time.mktime(l[0])):
                if i == 999:
                    continue
                writeline = {
                    'Date': time.strftime('%d/%m/%Y', txn[0]),
                    'Description': txn[1],
                    'Amount': txn[2]
                }
                writer.writerow(writeline)
                transactions.remove(txn)
                i += 1

            if i == 999:
                continue


if __name__ == '__main__':
    main()
