# src/scraper.py
import json
import logging
import os
from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from thordata import ThordataClient
from thordata.exceptions import ThordataNetworkError

from .config import DEFAULT_TIMEOUT, POLL_INTERVAL, SPIDER_CONFIG

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
            public_key=self.public_key,
        )

        self._http = requests.Session()
        retry = Retry(
            total=5, connect=5, read=5, backoff_factor=0.6,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"], raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._http.mount("https://", adapter)
        self._http.mount("http://", adapter)

    def _download_json(self, url: str) -> Any:
        resp = self._http.get(url, timeout=60)
        resp.raise_for_status()

        text = resp.text.strip()
        if not text:
            raise ValueError("Empty response from server")

        # Try standard JSON first
        try:
            return resp.json()
        except json.JSONDecodeError as e:
            # If standard JSON fails, try NDJSON (one JSON per line)
            try:
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                if not lines:
                    raise ValueError("No valid JSON lines found")
                
                # Try parsing as NDJSON
                parsed = [json.loads(line) for line in lines]
                # If we got multiple objects, return as list
                # If single object, return as dict (for backward compatibility)
                if len(parsed) == 1:
                    return parsed[0]
                return parsed
            except (json.JSONDecodeError, ValueError):
                # Last resort: try to parse multiple concatenated JSON objects
                try:
                    decoder = json.JSONDecoder()
                    idx = 0
                    out = []
                    while idx < len(text):
                        # Skip whitespace/newlines
                        while idx < len(text) and text[idx].isspace():
                            idx += 1
                        if idx >= len(text):
                            break
                        try:
                            obj, end = decoder.raw_decode(text, idx)
                            out.append(obj)
                            idx = end
                        except json.JSONDecodeError:
                            # If we can't parse from this position, break
                            break
                    
                    if out:
                        # Return single object if only one, otherwise return list
                        return out[0] if len(out) == 1 else out
                    raise ValueError(f"Could not parse JSON: {str(e)}")
                except Exception as parse_error:
                    logger.error(f"Failed to parse JSON response: {parse_error}")
                    logger.error(f"Response text (first 500 chars): {text[:500]}")
                    raise ValueError(f"JSON parsing failed: {str(e)}. Additional error: {str(parse_error)}")

    def _run(self, mode: str, params: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Any:
        cfg = SPIDER_CONFIG.get(mode)
        if not cfg:
            raise ValueError(f"Invalid mode: {mode}")

        logger.info(f"Amazon {mode}: {cfg['desc']}")
        
        try:
            result_url = self.client.run_task(
                file_name=f"amz_{mode}_{os.getpid()}",
                spider_id=cfg["id"], spider_name=cfg["name"], parameters=params,
                max_wait=DEFAULT_TIMEOUT, initial_poll_interval=POLL_INTERVAL,
            )
            logger.info("Finished! Downloading...")
            return self._download_json(result_url)

        except Exception as e:
            task_id = "N/A"
            if isinstance(e, ThordataNetworkError):
                msg = str(e)
                if msg.startswith("Task "):
                    parts = msg.split()
                    if len(parts) > 1: task_id = parts[1]

            error_details = {
                "error": str(e), "error_type": type(e).__name__, "task_id": task_id,
                "spider_id": cfg["id"], "parameters": params,
            }
            logger.error(f"Scraping task failed: {error_details}")
            return error_details

    # ========================================
    # 1. Amazon Product Details Scraper
    # ========================================
    def product_by_asin(self, params: Union[Dict, List]) -> Any:
        return self._run("product_by_asin", params)

    def product_by_url(self, params: Union[Dict, List]) -> Any:
        return self._run("product_by_url", params)

    def product_by_keywords(self, params: Union[Dict, List]) -> Any:
        return self._run("product_by_keywords", params)

    def product_by_category_url(self, params: Union[Dict, List]) -> Any:
        return self._run("product_by_category_url", params)

    def product_by_best_sellers(self, params: Union[Dict, List]) -> Any:
        return self._run("product_by_best_sellers", params)

    # ========================================
    # 2. Amazon Global Product Details Scraper
    # ========================================
    def global_product_by_url(self, params: Union[Dict, List]) -> Any:
        return self._run("global_product_by_url", params)

    def global_product_by_category_url(self, params: Union[Dict, List]) -> Any:
        return self._run("global_product_by_category_url", params)

    def global_product_by_seller_url(self, params: Union[Dict, List]) -> Any:
        return self._run("global_product_by_seller_url", params)

    def global_product_by_keywords(self, params: Union[Dict, List]) -> Any:
        return self._run("global_product_by_keywords", params)

    def global_product_by_keywords_brand(self, params: Union[Dict, List]) -> Any:
        return self._run("global_product_by_keywords_brand", params)

    # ========================================
    # 3. Amazon Product Review Scraper
    # ========================================
    def reviews_by_url(self, params: Union[Dict, List]) -> Any:
        return self._run("reviews_by_url", params)

    # ========================================
    # 4. Amazon Seller Information Scraper
    # ========================================
    def seller_by_url(self, params: Union[Dict, List]) -> Any:
        return self._run("seller_by_url", params)

    # ========================================
    # 5. Amazon Product Listing Scraper
    # ========================================
    def listing_by_keywords(self, params: Union[Dict, List]) -> Any:
        return self._run("listing_by_keywords", params)
