import os
import sys

# Call app.pyw
current_dir = os.path.dirname(os.path.abspath(__file__))
pyw_path = os.path.join(current_dir, "app.pyw")
with open(pyw_path, "r", encoding="utf-8") as f:
    code = f.read()

exec(code)
