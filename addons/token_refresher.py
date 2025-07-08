import json
import logging
import os
import socket
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

_LOGGER = logging.getLogger(__name__)      

def resolve_host():
    """Try to resolve host.docker.internal, fallback to UGREEN_NAS_API_IP or localhost."""
    try:
        return socket.gethostbyname("host.docker.internal")
    except socket.gaierror:
        return os.getenv("UGREEN_NAS_API_IP", "127.0.0.1")
        
class TokenRefresher:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._scheme = os.environ.get("UGREEN_NAS_API_SCHEME", "https")
        self._host = resolve_host()
        self._port = int(os.environ.get("UGREEN_NAS_API_PORT") or "9999")
        self._verify = os.environ.get("UGREEN_NAS_API_VERIFY_SSL", "true").lower() == "true"
        self._token = None

    @property
    def token(self):
        return self._token

    async def fetch_token_async(self) -> bool:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(ignore_https_errors=not self._verify)
            page = await context.new_page()

            url = f"{self._scheme}://{self._host}:{self._port}"
            _LOGGER.info("Navigating to %s", url)
            await page.goto(url, wait_until="domcontentloaded")

            await page.fill('input[name="ugos-username"]', self._username)
            await page.fill('input[name="ugos-password"]', self._password)

            checkbox_selector = 'div.is-login input[type="checkbox"]'
            if not await page.is_checked(checkbox_selector):
                await page.check(checkbox_selector)

            await page.wait_for_selector('.login-public-button button[type="button"]:not([disabled])')
            await page.click('.login-public-button button[type="button"]')

            try:
                await page.wait_for_selector('div.dashboard', timeout=5000)
            except PlaywrightTimeoutError:
                _LOGGER.warning("Login confirmation not found, waiting fallback timeout.")
                await page.wait_for_timeout(3000)

            local_storage = await page.evaluate("Object.assign({}, window.localStorage);")

            for value in local_storage.values():
                if 'api_token' in value:
                    try:
                        json_data = json.loads(value)
                        token = json_data.get("accessInfo", {}).get("api_token")
                        if token:
                            self._token = token
                            _LOGGER.info("API token successfully retrieved.")
                            return True
                    except json.JSONDecodeError as e:
                        _LOGGER.debug("Invalid JSON in localStorage: %s", e)

            _LOGGER.error("API token not found in localStorage.")
            return False