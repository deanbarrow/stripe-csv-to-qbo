stripe-csv-to-qbo
=================
Converts CSV exports from Stripe to a CSV format that QuickBooks Online understands.

Stripe Download
---------------

1. In your Stripe account, browse to the Balance → Transactions page.
2. Filter to the required time range then click Export, you'll end up with a CSV file (probably called `payments.csv`).

Convert
-------

1. Run `python stripe2qbo.py payments.csv` (note that if you have multiple CSV files from Stripe you can add/specify them all). The script will output a file named `StripeQuickBooksOutput[num].csv`. If the number of transactions are greater than 999 it will create multiple output files as QBO only allows CSV imports of up to 1000 lines (headers + 999 transactions).

QuickBooks Online Upload
------------------------

1. In your Quickbooks Online account, go to the account you want to import transactions into.
2. Click the arrow next to the "Update" button in the upper right and select "File Upload".
3. Click the Browse button and find the `StripeQuickBooksOutput[num].csv` file generated above.

Other
-----

Inspired by https://github.com/iandees/csv-to-qbo

Tested and working with UK Stripe/Quickbooks accounts.

See also a Paypal version https://github.com/deanbarrow/paypal-csv-to-qbo
