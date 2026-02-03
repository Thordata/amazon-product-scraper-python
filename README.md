# Amazon Product Scraper for Python

<div align="center">

<img src="https://img.shields.io/badge/Thordata-Official-blue?style=for-the-badge" alt="Thordata Logo">

**Extract prices, ASINs, reviews, and seller data from Amazon at scale.**  
*Powered by Thordata's residential proxy network & Web Scraper API.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Powered By](https://img.shields.io/badge/Powered%20By-Thordata-orange)](https://dashboard.thordata.com/?utm_source=github&utm_medium=readme&utm_campaign=amazon_scraper)

</div>

---

## ⚡ Features

- **📦 Product Details**: Scrape by ASIN, URL, keywords, category, and best sellers.
- **🌍 Global Products**: Scrape global products by URL, category, seller, keywords, and brand.
- **⭐ Reviews**: Get user reviews, ratings, and dates.
- **🏬 Seller Info**: Extract seller details and business profiles.
- **📈 Product Listings**: Get product listings by keyword and domain.
- **🛡️ Anti-Bot Bypass**: Automatically handles CAPTCHAs, IP rotation, and headers.
- **批量支持**: 大多数爬虫都支持批量模式，可一次性提交多个任务。

## 🚀 Quick Start

### 1. Get Credentials

Get your **free** scraping token from the [Thordata Dashboard](https://dashboard.thordata.com/?utm_source=github&utm_medium=readme&utm_campaign=amazon_scraper).

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

#### 1. Amazon Product Details Scraper

**By ASIN:**
```bash
python main.py product asin B0BZYCJK89
```

**By URL (with optional zip_code):**
```bash
python main.py product url "https://www.amazon.com/dp/B0BRXPR726" --zip-code 94107
```

**By Keywords:**
```bash
python main.py product keywords "Apple Watch" --page-turning 2 --lowest-price 1 --highest-price 10000
```

#### 2. Amazon Global Product Details Scraper

**By URL:**
```bash
python main.py global url "https://www.amazon.com/dp/B0CHHSFMRL/"
```

#### 3. Amazon Product Review Scraper

```bash
python main.py reviews "https://www.amazon.com/dp/B0BRXPR726"
```

#### 4. Amazon Seller Information Scraper

```bash
python main.py seller "https://www.amazon.com/sp?ie=UTF8&seller=A3AZYNALJBV2WE&asin=B099S46ZRQ"
```

#### 5. Amazon Product Listing Scraper

```bash
python main.py listing "X-box" "https://www.amazon.com/" --page-turning 1
```

All data is saved to `output/` in JSON format.

---

## 🏗️ How it Works

This scraper uses **Thordata's Web Scraper API (Hybrid Mode)**:
1.  **Task Creation**: Sends scraping parameters to Thordata's cloud cluster.
2.  **Auto-Polling**: The SDK (`run_task`) automatically polls for completion.
3.  **Result Retrieval**: Downloads the clean JSON data once ready.

This architecture ensures you **never get blocked** and receive clean, structured data.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

