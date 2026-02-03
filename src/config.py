# src/config.py

# Spider ID Configuration (Verified from Thordata Dashboard)
SPIDER_CONFIG = {
    # ========================================
    # 1. Amazon Product Details Scraper
    # ========================================
    "product_by_asin": {
        "id": "amazon_product_by-asin",
        "name": "amazon.com",
        "desc": "Get product details by ASIN",
        "input_keys": ["asin"],
    },
    "product_by_url": {
        "id": "amazon_product_by-url",
        "name": "amazon.com",
        "desc": "Get product details by URL (zip_code optional)",
        "input_keys": ["url", "zip_code"],
    },
    "product_by_keywords": {
        "id": "amazon_product_by-keywords",
        "name": "amazon.com",
        "desc": "Search products by keywords with price range",
        "input_keys": ["keyword", "page_turning", "lowest_price", "highest_price"],
    },
    "product_by_category_url": {
        "id": "amazon_product_by-category-url",
        "name": "amazon.com",
        "desc": "Get products by category URL with sorting",
        "input_keys": ["url", "page_turning", "sort_by"],
    },
    "product_by_best_sellers": {
        "id": "amazon_product_by-best-sellers",
        "name": "amazon.com",
        "desc": "Get best sellers listing",
        "input_keys": ["url", "page_turning"],
    },

    # ========================================
    # 2. Amazon Global Product Details Scraper
    # ========================================
    "global_product_by_url": {
        "id": "amazon_global-product_by-url",
        "name": "amazon.com",
        "desc": "Get global product details by URL",
        "input_keys": ["url"],
    },
    "global_product_by_category_url": {
        "id": "amazon_global-product_by-category-url",
        "name": "amazon.com",
        "desc": "Get global products by category URL",
        "input_keys": ["url", "maximum", "sort_by", "get_sponsored"],
    },
    "global_product_by_seller_url": {
        "id": "amazon_global-product_by-seller-url",
        "name": "amazon.com",
        "desc": "Get global products by seller URL",
        "input_keys": ["url", "maximum"],
    },
    "global_product_by_keywords": {
        "id": "amazon_global-product_by-keywords",
        "name": "amazon.com",
        "desc": "Search global products by keywords",
        "input_keys": ["keyword", "domain", "lowest_price", "highest_price", "page_turning"],
    },
    "global_product_by_keywords_brand": {
        "id": "amazon_global-product_by-keywords-brand",
        "name": "amazon.com",
        "desc": "Search global products by keywords and brand",
        "input_keys": ["keyword", "brands", "page_turning"],
    },

    # ========================================
    # 3. Amazon Product Review Scraper
    # ========================================
    "reviews_by_url": {
        "id": "amazon_comment_by-url",
        "name": "amazon.com",
        "desc": "Get product reviews by URL",
        "input_keys": ["url"],
    },

    # ========================================
    # 4. Amazon Product Listing Scraper
    # ========================================
    "listing_by_keywords": {
        "id": "amazon_product-list_by-keywords-domain",
        "name": "amazon.com",
        "desc": "Get product listing by keywords and domain",
        "input_keys": ["keyword", "domain", "page_turning"],
    },

    # ========================================
    # 5. Amazon Seller Information Scraper
    # ========================================
    "seller_by_url": {
        "id": "amazon_seller_by-url",
        "name": "amazon.com",
        "desc": "Get seller information by URL",
        "input_keys": ["url"],
    },
}

DEFAULT_TIMEOUT = 600
POLL_INTERVAL = 3
