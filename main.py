import argparse
import json
import os
import sys
import time
from typing import Any

# Add project root to Python path to ensure src module is found
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv

from src.scraper import AmazonScraper

load_dotenv()


def _now_ts() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def save_json(data: Any, name: str) -> str:
    os.makedirs("output", exist_ok=True)
    path = f"output/{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {path}")
    return path


def save_error(data: Any, name: str) -> str:
    os.makedirs("output", exist_ok=True)
    path = f"output/error_{name}_{_now_ts()}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved error to {path}")
    return path


def save_result(data: Any, name: str) -> None:
    if isinstance(data, dict) and data.get("error"):
        save_error(data, name)
        raise SystemExit(data.get("error"))
    save_json(data, name)


SORT_BY_CHOICES = [
    "Best Sellers",
    "Newest Arrivals",
    "Avg. Customer Review",
    "Price: High to Low",
    "Price: Low to High",
    "Featured",
]


def main():
    parser = argparse.ArgumentParser(description="Amazon scraper powered by Thordata")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # ==========================================================
    # 1) Amazon Product Details Scraper
    # ==========================================================
    product = sub.add_parser("product", help="Amazon Product Details Scraper")
    product_sub = product.add_subparsers(dest="product_cmd", required=True)

    p_asin = product_sub.add_parser("asin", help="amazon_product_by-asin")
    p_asin.add_argument("asin", help="ASIN, e.g. B0BZYCJK89")

    p_url = product_sub.add_parser("url", help="amazon_product_by-url")
    p_url.add_argument("url", help="Product URL")
    p_url.add_argument("--zip-code", default=None, help="Optional zip_code")

    p_keywords = product_sub.add_parser("keywords", help="amazon_product_by-keywords")
    p_keywords.add_argument("keyword", help="Keyword, e.g. Apple Watch")
    p_keywords.add_argument("--page-turning", default="1", help="Page turning, default 1")
    p_keywords.add_argument("--lowest-price", default=None, help="Optional lowest_price")
    p_keywords.add_argument("--highest-price", default=None, help="Optional highest_price")

    p_category = product_sub.add_parser("category-url", help="amazon_product_by-category-url")
    p_category.add_argument("url", nargs="?", default=None, help="Category URL")
    p_category.add_argument("--page-turning", default="1", help="Page turning, default 1")
    p_category.add_argument("--sort-by", choices=SORT_BY_CHOICES, default=None, help="Optional sort_by")
    p_category.add_argument("--batch-file", default=None, help="Path to a JSON file for batch processing")

    p_bestsellers = product_sub.add_parser("best-sellers", help="amazon_product_by-best-sellers")
    p_bestsellers.add_argument("url", help="Best sellers URL")
    p_bestsellers.add_argument("--page-turning", default="1", help="Page turning, default 1")

    # ==========================================================
    # 2) Amazon Global Product Details Scraper
    # ==========================================================
    global_p = sub.add_parser("global", help="Amazon Global Product Details Scraper")
    global_sub = global_p.add_subparsers(dest="global_cmd", required=True)

    g_url = global_sub.add_parser("url", help="amazon_global-product_by-url")
    g_url.add_argument("url", help="Global product URL")

    g_category = global_sub.add_parser("category-url", help="amazon_global-product_by-category-url")
    g_category.add_argument("url", help="Category URL")
    g_category.add_argument("--maximum", default=None, help="Optional maximum")
    g_category.add_argument("--sort-by", default=None, help="Optional sort_by")
    g_category.add_argument("--get-sponsored", default=None, help="Optional get_sponsored (true/false)")

    g_seller = global_sub.add_parser("seller-url", help="amazon_global-product_by-seller-url")
    g_seller.add_argument("url", help="Seller URL")
    g_seller.add_argument("--maximum", default=None, help="Optional maximum")

    g_keywords = global_sub.add_parser("keywords", help="amazon_global-product_by-keywords")
    g_keywords.add_argument("keyword", help="Keyword, e.g. coffee")
    g_keywords.add_argument("--domain", required=True, help="Domain, e.g. https://www.amazon.com")
    g_keywords.add_argument("--page-turning", default="1", help="Page turning, default 1")
    g_keywords.add_argument("--lowest-price", default=None, help="Optional lowest_price")
    g_keywords.add_argument("--highest-price", default=None, help="Optional highest_price")

    g_brand = global_sub.add_parser("keywords-brand", help="amazon_global-product_by-keywords-brand")
    g_brand.add_argument("keyword", help="Keyword, e.g. shirts")
    g_brand.add_argument("--brands", required=True, help="Brands, e.g. Adidas")
    g_brand.add_argument("--page-turning", default="1", help="Page turning, default 1")

    # ==========================================================
    # 3) Amazon Product Review Scraper
    # ==========================================================
    reviews = sub.add_parser("reviews", help="Amazon Product Review Scraper")
    reviews.add_argument("url", help="Product URL")

    # ==========================================================
    # 4) Amazon Seller Information Scraper
    # ==========================================================
    seller = sub.add_parser("seller", help="Amazon Seller Information Scraper")
    seller.add_argument("url", help="Seller URL")

    # ==========================================================
    # 5) Amazon Product Listing Scraper
    # ==========================================================
    listing = sub.add_parser("listing", help="Amazon Product Listing Scraper")
    listing.add_argument("keyword", help="Keyword, e.g. X-box")
    listing.add_argument("domain", help="Domain, e.g. https://www.amazon.com/")
    listing.add_argument("--page-turning", default="1", help="Page turning, default 1")

    args = parser.parse_args()
    bot = AmazonScraper()

    if args.cmd == "product":
        if args.product_cmd == "asin":
            save_result(bot.product_by_asin({"asin": args.asin}), "product_by_asin")
        elif args.product_cmd == "url":
            params = {"url": args.url}
            if args.zip_code: params["zip_code"] = args.zip_code
            save_result(bot.product_by_url(params), "product_by_url")
        elif args.product_cmd == "keywords":
            params = {"keyword": args.keyword, "page_turning": args.page_turning}
            if args.lowest_price: params["lowest_price"] = args.lowest_price
            if args.highest_price: params["highest_price"] = args.highest_price
            save_result(bot.product_by_keywords(params), "product_by_keywords")
        elif args.product_cmd == "category-url":
            if args.batch_file:
                batch = json.load(open(args.batch_file, "r", encoding="utf-8"))
                save_result(bot.product_by_category_url(batch), "product_by_category_url_batch")
            else:
                params = {"url": args.url, "page_turning": args.page_turning}
                if args.sort_by: params["sort_by"] = args.sort_by
                save_result(bot.product_by_category_url(params), "product_by_category_url")
        elif args.product_cmd == "best-sellers":
            save_result(bot.product_by_best_sellers({"url": args.url, "page_turning": args.page_turning}), "product_by_best_sellers")

    elif args.cmd == "global":
        if args.global_cmd == "url":
            save_result(bot.global_product_by_url({"url": args.url}), "global_product_by_url")
        elif args.global_cmd == "category-url":
            params = {"url": args.url}
            if args.maximum: params["maximum"] = args.maximum
            if args.sort_by: params["sort_by"] = args.sort_by
            if args.get_sponsored: params["get_sponsored"] = args.get_sponsored
            save_result(bot.global_product_by_category_url(params), "global_product_by_category_url")
        elif args.global_cmd == "seller-url":
            params = {"url": args.url}
            if args.maximum: params["maximum"] = args.maximum
            save_result(bot.global_product_by_seller_url(params), "global_product_by_seller_url")
        elif args.global_cmd == "keywords":
            params = {"keyword": args.keyword, "domain": args.domain, "page_turning": args.page_turning}
            if args.lowest_price: params["lowest_price"] = args.lowest_price
            if args.highest_price: params["highest_price"] = args.highest_price
            save_result(bot.global_product_by_keywords(params), "global_product_by_keywords")
        elif args.global_cmd == "keywords-brand":
            save_result(bot.global_product_by_keywords_brand({"keyword": args.keyword, "brands": args.brands, "page_turning": args.page_turning}), "global_product_by_keywords_brand")

    elif args.cmd == "reviews":
        save_result(bot.reviews_by_url({"url": args.url}), "reviews")

    elif args.cmd == "seller":
        save_result(bot.seller_by_url({"url": args.url}), "seller")

    elif args.cmd == "listing":
        # argparse converts --page-turning to page_turning attribute
        page_turning = getattr(args, "page_turning", "1")
        save_result(bot.listing_by_keywords({"keyword": args.keyword, "domain": args.domain, "page_turning": page_turning}), "listing")

if __name__ == "__main__":
    main()
