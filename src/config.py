# src/config.py

# Spider ID Configuration (Verified from Dashboard Inputs)
SPIDER_CONFIG = {
    # 1. Product by ASIN (最精准)
    "product_asin": {
        "id": "amazon_product_by-asin",
        "name": "amazon.com",
        "desc": "Get product details by ASIN",
        "input_keys": ["asin"]
    },
    # 2. Product by URL (全球通用)
    "product_url": {
        "id": "amazon_global-product_by-url",
        "name": "amazon.com",
        "desc": "Get product details by URL (Global)",
        "input_keys": ["url"]
    },
    # 3. Reviews (评论)
    "reviews": {
        "id": "amazon_comment_by-url",
        "name": "amazon.com",
        "desc": "Get product reviews",
        "input_keys": ["url"]
    },
    # 4. Search (Listing)
    "search": {
        "id": "amazon_product-list_by-keywords-domain",
        "name": "amazon.com",
        "desc": "Search keywords on Amazon",
        "input_keys": ["keyword", "domain", "page_turning"]
    },
    # 5. Seller (卖家信息)
    "seller": {
        "id": "amazon_seller_by-url",
        "name": "amazon.com",
        "desc": "Get seller information",
        "input_keys": ["url"]
    }
}

DEFAULT_TIMEOUT = 600
POLL_INTERVAL = 3