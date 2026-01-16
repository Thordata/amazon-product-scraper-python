# Amazon Product Scraper for Python

<div align="center">

<img src="https://img.shields.io/badge/Thordata-Official-blue?style=for-the-badge" alt="Thordata Logo">

**Extract prices, ASINs, reviews, and seller data from Amazon at scale.**  
*Powered by Thordata's residential proxy network & Web Scraper API.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Powered By](https://img.shields.io/badge/Powered%20By-Thordata-orange)](https://www.thordata.com/?utm_source=github&utm_medium=readme&utm_campaign=amazon_scraper)

</div>

---

## ⚡ Features

*   **📦 Product Details**: Scrape title, price, rating, description, and images by ASIN or URL.
*   **🔍 Search & Listing**: Extract product lists from keywords (e.g., "Gaming Laptop").
*   **⭐ Reviews**: Get user reviews, ratings, and dates.
*   **store Seller Info**: Extract seller details and business profiles.
*   **🛡️ Anti-Bot Bypass**: Automatically handles CAPTCHAs, IP rotation, and headers.
*   **🌍 Global Support**: Works with `.com`, `.co.uk`, `.co.jp`, `.de`, etc.

## 🚀 Quick Start

### 1. Get Credentials
Get your **free** scraping token from the [Thordata Dashboard](https://www.thordata.com/?utm_source=github&utm_medium=readme&utm_campaign=amazon_scraper).

### 2. Install
```bash
git clone https://github.com/Thordata/amazon-product-scraper-python.git
cd amazon-product-scraper-python
pip install -r requirements.txt
```

### 3. Configure
Copy `.env.example` to `.env` and fill in your tokens:
```ini
THORDATA_SCRAPER_TOKEN=your_token
THORDATA_PUBLIC_TOKEN=your_public
THORDATA_PUBLIC_KEY=your_key
```

### 4. Run Examples

**Search Products:**
```bash
python main.py search "iPhone 15 Case" --pages 2
```

**Get Details (by ASIN):**
```bash
python main.py product "B0CHHSFMRL"
```

**Get Details (by URL):**
```bash
python main.py product "https://www.amazon.com/dp/B0CHHSFMRL"
```

**Get Reviews:**
```bash
python main.py reviews "https://www.amazon.com/dp/B0CHHSFMRL"
```

**Get Seller Info:**
```bash
python main.py seller "https://www.amazon.com/sp?seller=..."
```

All data is saved to `output/` in JSON format.

---

## 🏗️ How it Works

This scraper uses **Thordata's Web Scraper API (Hybrid Mode)**:
1.  **Task Creation**: Sends scraping parameters to Thordata's cloud cluster.
2.  **Auto-Polling**: The SDK (`run_task`) automatically polls for completion.
3.  **Result Retrieval**: Downloads the clean JSON data once ready.

This architecture ensures you **never get IP blocked** and don't need to maintain local headless browsers.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.