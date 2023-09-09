import pandas as pd

data = pd.read_excel("CustomerInvoices.xlsx")

invoices = data["Invoice"].mean()

print(invoices)

