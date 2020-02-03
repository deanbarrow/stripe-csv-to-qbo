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
            tstamp = time.strptime('{created_utc}'.format(**line), '%Y-%m-%d %H:%M:%S')
            line['gross'] = line['gross'].replace(',','')

            if line['reporting_category'] == 'payout':
                transactions.append((tstamp, 'Transfer: {description}'.format(**line), line['gross']))

            elif line['reporting_category'] == 'refund':
                transactions.append((tstamp, 'Refund: {description} From {customer_description} {customer_email}'.format(**line), line['gross']))

                if line['fee'] != '0.00':
                    transactions.append((tstamp, 'Refund: Fee {description} From {customer_description} {customer_email}'.format(**line), ('-' + line['fee']).replace('--','')))

            elif line['reporting_category'] == 'adjustment':
                transactions.append((tstamp, 'Adjustment: {description} From {customer_description} {customer_email}'.format(**line), line['gross']))

                if line['fee'] != '0.00':
                    transactions.append((tstamp, 'Adjustment: Fee {description} From {customer_description} {customer_email}'.format(**line), ('-' + line['fee']).replace('--','')))

            elif line['reporting_category'] == 'charge':
                transactions.append((tstamp, 'Received: {description} From {customer_description} {customer_email}'.format(**line), line['gross']))

                if line['fee'] != '0.00':
                    transactions.append((tstamp, 'Spent: Fee {description} From {customer_description} {customer_email}'.format(**line), ('-' + line['fee']).replace('--','')))

            else: 
                transactions.append((tstamp, 'REVIEW: {id} {description} From {customer_description} {customer_email}'.format(**line), line['gross']))
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
