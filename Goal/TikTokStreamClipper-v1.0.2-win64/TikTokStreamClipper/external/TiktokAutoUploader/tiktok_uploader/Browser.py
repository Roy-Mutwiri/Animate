from .cookies import load_cookies_from_file, save_cookies_to_file
from fake_useragent import UserAgent, FakeUserAgentError
import undetected_chromedriver as uc
import subprocess, threading, os, re, sys


WITH_PROXIES = False
_ORIGINAL_CHROME_DEL = getattr(uc.Chrome, "__del__", None)


def _safe_chrome_del(self):
    if _ORIGINAL_CHROME_DEL is None:
        return
    try:
        _ORIGINAL_CHROME_DEL(self)
    except Exception:
        # undetected_chromedriver can raise during interpreter cleanup on
        # Windows after Chrome has already closed. That exception is not
        # actionable and otherwise appears as "Exception ignored in __del__".
        return


uc.Chrome.__del__ = _safe_chrome_del


def _get_chrome_major_version() -> int:
    """Detect the major version of the system-installed Chrome/Chromium so
    undetected-chromedriver downloads the matching ChromeDriver binary."""
    for binary in (
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "chrome",
        "chrome.exe",
    ):
        try:
            out = subprocess.check_output([binary, "--version"], stderr=subprocess.DEVNULL).decode()
            version = _extract_major_version(out)
            if version:
                return version
        except (FileNotFoundError, ValueError, IndexError):
            continue
    if sys.platform.startswith("win"):
        for path in (
            os.path.join(os.environ.get("PROGRAMFILES", ""), "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
        ):
            if not path or not os.path.exists(path):
                continue
            try:
                escaped_path = path.replace("'", "''")
                ps = (
                    f"(Get-Item -LiteralPath '{escaped_path}')."
                    "VersionInfo.ProductVersion"
                )
                out = subprocess.check_output(
                    ["powershell", "-NoProfile", "-Command", ps],
                    stderr=subprocess.DEVNULL,
                ).decode()
                version = _extract_major_version(out)
                if version:
                    return version
            except (subprocess.SubprocessError, ValueError):
                continue
    return 0  # fall back to latest if detection fails


def _extract_major_version(value: str) -> int:
    match = re.search(r"(\d+)\.", value or "")
    return int(match.group(1)) if match else 0


class Browser:
    __instance = None

    @staticmethod
    def get():
        # print("Browser.getBrowser() called")
        if Browser.__instance is None:
            with threading.Lock():
                if Browser.__instance is None:
                    # print("Creating new browser instance due to no instance found")
                    Browser.__instance = Browser()
        return Browser.__instance

    def __init__(self):
        if Browser.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Browser.__instance = self
        self.user_agent = ""
        options = uc.ChromeOptions()
        # Proxies not supported on login.
        # if WITH_PROXIES:
        #     options.add_argument('--proxy-server={}'.format(PROXIES[0]))
        self._driver = uc.Chrome(options=options, version_main=_get_chrome_major_version())
        self.with_random_user_agent()

    def with_random_user_agent(self, fallback=None):
        """Set random user agent.
        NOTE: This could fail with `FakeUserAgentError`.
        Provide `fallback` str to set the user agent to the provided string, in case it fails. 
        If fallback is not provided the exception is re-raised"""

        try:
            self.user_agent = UserAgent().random
        except FakeUserAgentError as e:
            if fallback:
                self.user_agent = fallback
            else:
                raise e

    @property
    def driver(self):
        return self._driver

    def close(self):
        try:
            self._driver.quit()
        except Exception:
            pass
        finally:
            Browser.__instance = None

    def load_cookies_from_file(self, filename):
        cookies = load_cookies_from_file(filename)
        for cookie in cookies:
            self._driver.add_cookie(cookie)
        self._driver.refresh()

    def save_cookies(self, filename: str, cookies:list=None):
        save_cookies_to_file(cookies, filename)


if __name__ == "__main__":
    import os
    # get current relative path of this file.
    print(os.path.dirname(os.path.abspath(__file__)))
