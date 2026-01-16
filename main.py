import argparse
import json
import os
from dotenv import load_dotenv
from src.scraper import AmazonScraper

load_dotenv()

def save(data, name):
    os.makedirs("output", exist_ok=True)
    path = f"output/{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {path}")

def main():
    parser = argparse.ArgumentParser(description="Amazon Scraper powered by Thordata")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Search
    search = sub.add_parser("search", help="Search products")
    search.add_argument("keyword", help="e.g. 'Laptop'")
    search.add_argument("--domain", default="https://www.amazon.com/", help="Amazon domain")
    search.add_argument("--pages", type=int, default=1, help="Pages to scrape")

    # Product
    prod = sub.add_parser("product", help="Get product details")
    prod.add_argument("target", help="ASIN (e.g. B08...) or URL")

    # Reviews
    rev = sub.add_parser("reviews", help="Get reviews")
    rev.add_argument("url", help="Product URL")

    # Seller
    sell = sub.add_parser("seller", help="Get seller info")
    sell.add_argument("url", help="Seller URL")

    args = parser.parse_args()
    bot = AmazonScraper()

    if args.cmd == "search":
        data = bot.search(args.keyword, args.domain, args.pages)
        save(data, f"search_{args.keyword}")
    elif args.cmd == "product":
        data = bot.get_product(args.target)
        save(data, "product_details")
    elif args.cmd == "reviews":
        data = bot.get_reviews(args.url)
        save(data, "reviews")
    elif args.cmd == "seller":
        data = bot.get_seller(args.url)
        save(data, "seller")

if __name__ == "__main__":
    main()