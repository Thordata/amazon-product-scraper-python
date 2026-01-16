# src/scraper.py
import os
import logging
from typing import Dict, Any, List
from thordata import ThordataClient
from .config import SPIDER_CONFIG, DEFAULT_TIMEOUT, POLL_INTERVAL

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AmazonScraper")

class AmazonScraper:
    def __init__(self):
        self.api_key = os.getenv("THORDATA_SCRAPER_TOKEN")
        self.public_token = os.getenv("THORDATA_PUBLIC_TOKEN")
        self.public_key = os.getenv("THORDATA_PUBLIC_KEY")
        
        if not all([self.api_key, self.public_token, self.public_key]):
            raise ValueError("Missing required tokens in .env")
            
        self.client = ThordataClient(
            scraper_token=self.api_key,
            public_token=self.public_token,
            public_key=self.public_key
        )

    def _run(self, mode: str, params: Dict[str, Any]) -> Dict:
        cfg = SPIDER_CONFIG.get(mode)
        if not cfg: raise ValueError(f"Invalid mode: {mode}")

        logger.info(f"🛒 Amazon {mode}: {cfg['desc']}")
        
        try:
            # SDK 1.2.0 run_task
            result_url = self.client.run_task(
                file_name=f"amz_{mode}_{os.getpid()}",
                spider_id=cfg["id"],
                spider_name=cfg["name"],
                parameters=params,
                max_wait=DEFAULT_TIMEOUT,
                initial_poll_interval=POLL_INTERVAL
            )
            
            logger.info(f"✅ Finished! Downloading...")
            import requests
            return requests.get(result_url).json()
        except Exception as e:
            logger.error(f"❌ Failed: {e}")
            return {"error": str(e)}

    def search(self, keyword: str, domain: str = "https://www.amazon.com/", pages: int = 1):
        """Search products by keyword"""
        return self._run("search", {
            "keyword": keyword,
            "domain": domain,
            "page_turning": str(pages)
        })

    def get_product(self, target: str):
        """Smartly detect if ASIN or URL"""
        if target.startswith("http"):
            return self._run("product_url", {"url": target})
        else:
            return self._run("product_asin", {"asin": target})

    def get_reviews(self, url: str):
        return self._run("reviews", {"url": url})

    def get_seller(self, url: str):
        return self._run("seller", {"url": url})