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
            tstamp = time.strptime('{Created (UTC)}'.format(**line), '%Y-%m-%d %H:%M')
            line['Amount'] = line['Amount'].replace(',','')

            if line['Type'] == 'transfer':
                transactions.append((tstamp, 'Transfer: {Description}'.format(**line), line['Amount']))

            elif line['Type'] == 'refund':
                transactions.append((tstamp, 'Refund: {Description} From {Customer Name (metadata)} {Customer Email (metadata)}'.format(**line), line['Amount']))

                if line['Fee'] != '0.00':
                    transactions.append((tstamp, 'Refund: Fee {Description} From {Customer Name (metadata)} {Customer Email (metadata)}'.format(**line), ('-' + line['Fee']).replace('--','')))

            elif line['Type'] == 'adjustment':
                transactions.append((tstamp, 'Adjustment: {Description} From {Customer Name (metadata)} {Customer Email (metadata)}'.format(**line), line['Amount']))

                if line['Fee'] != '0.00':
                    transactions.append((tstamp, 'Adjustment: Fee {Description} From {Customer Name (metadata)} {Customer Email (metadata)}'.format(**line), ('-' + line['Fee']).replace('--','')))

            elif line['Type'] == 'charge':
                transactions.append((tstamp, 'Received: {Description} From {Customer Name (metadata)} {Customer Email (metadata)}'.format(**line), line['Amount']))

                if line['Fee'] != '0.00':
                    transactions.append((tstamp, 'Spent: Fee {Description} From {Customer Name (metadata)} {Customer Email (metadata)}'.format(**line), ('-' + line['Fee']).replace('--','')))

            else: 
                transactions.append((tstamp, 'REVIEW: {id} {Description} From {Customer Name (metadata)} {Customer Email (metadata)}'.format(**line), line['Amount']))
                print 'Review transaction ID {id}'.format(**line)

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
