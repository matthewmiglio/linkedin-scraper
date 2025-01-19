from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options


def make_firefox_driver():
    start_time = time.time()
    print("Creating firefox driver...")

    try:
        # Set Firefox options
        firefox_options = Options()

        firefox_options.add_argument('-headless')
        firefox_options.add_argument("--bwsi")
        firefox_options.add_argument("--mute-audio")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--arc-disable-app-sync")
        firefox_options.add_argument("--arc-disable-dexopt-cache")
        firefox_options.add_argument("--arc-disable-download-provider")
        firefox_options.add_argument("--arc-disable-play-auto-install")
        firefox_options.add_argument("--aggressive-cache-discard")
        firefox_options.add_argument("--allow-insecure-localhost")
        firefox_options.add_argument("--webview-force-disable-3pcs")
        firefox_options.add_argument("--stabilize-time-dependent-view-for-tests")
        firefox_options.add_argument("--site-per-process")
        firefox_options.add_argument("--show-taps")
        firefox_options.add_argument("--short-merge-session-timeout-for-test")
        firefox_options.add_argument("--short-reporting-delay")
        firefox_options.add_argument("--show-aggregated-damage")
        firefox_options.add_argument("--show-autofill-signatures")
        firefox_options.add_argument("--show-autofill-type-predictions")
        firefox_options.add_argument("--show-component-extension-options")
        firefox_options.add_argument("--show-composited-layer-borders")
        firefox_options.add_argument("--show-dc-layer-debug-borders")
        firefox_options.add_argument("--show-fps-counter")
        firefox_options.add_argument("--show-icons")
        firefox_options.add_argument("--show-layer-animation-bounds")
        firefox_options.add_argument("--show-layout-shift-regions")
        firefox_options.add_argument("--show-login-dev-overlay")
        firefox_options.add_argument("--show-mac-overlay-borders")
        firefox_options.add_argument("--show-oobe-dev-overlay")
        firefox_options.add_argument("--show-oobe-quick-start-debugger")
        firefox_options.add_argument("--show-overdraw-feedback")
        firefox_options.add_argument("--show-paint-rects")
        firefox_options.add_argument("--show-property-changed-rects")
        firefox_options.add_argument("--show-screenspace-rects")
        firefox_options.add_argument("--show-surface-damage-rects")
        firefox_options.add_argument("--blink-settings=imagesEnabled=false")
        firefox_options.add_argument("--disable-plugins")
        firefox_options.add_argument("--disable-javascript")
        firefox_options.add_argument("--disable-css")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable -dev-shm-usage")
        firefox_options.add_argument("--disable- software-rasterizer")
        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--disable-sync")
        firefox_options.add_argument("--disable-background-networking")
        firefox_options.add_argument("--disable-default-apps")
        firefox_options.add_argument("--disable-features=TranslateUI")
        firefox_options.add_argument("--disable-popup-blocking")
        firefox_options.add_argument("--mute-audio")
        firefox_options.add_argument("--disable-background-timer-throttling")
        firefox_options.add_argument("--disable-renderer-backgrounding")
        firefox_options.add_argument("--no-default-browser-check")

        driver = webdriver.Firefox(options=firefox_options)

        time_taken = str(time.time() - start_time).split(".")[0]
        print(
            f"Successfully created and configured firefox driver in {time_taken}s"
        )
        return driver
    except:
        print("Failed to create  or configure firefox driver")
        return None


def find_element_by_xpath(driver, xpath):
    return driver.find_element(By.XPATH, xpath)


def click_xpaths(driver, xpaths) -> bool:
    timeout = 5  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        for xpath in xpaths:
            try:
                find_element_by_xpath(driver, xpath).click()
                return True
            except:
                pass
    return False


def scroll_down(driver, scroll_pause_time=2, num_scrolls=5):
    try:
        # Get current page height
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down multiple times to load more content
        for _ in range(num_scrolls):
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load more content
            time.sleep(scroll_pause_time)

            # Calculate new page height after scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Break if no more content is loaded
            if new_height == last_height:
                break

            # Update last height
            last_height = new_height

    except Exception as e:
        print(f"Error while scrolling down: {str(e)}")


def send_keys(driver, xpaths, text):
    timeout = 5  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        for xpath in xpaths:
            try:
                find_element_by_xpath(driver, xpath).send_keys(text)
                return True
            except:
                pass
    return False


def get_text_from_xpaths(driver, xpaths):
    texts = []

    for xpath in xpaths:
        try:
            element = find_element_by_xpath(driver, xpath)
            text = element.text
            texts.append(text)
        except:
            pass

    return texts


def scroll_down_inside_element(driver, element, scroll_pause_time=2, num_scrolls=5) -> bool:
    try:
        # Get current scroll height of the element
        last_height = driver.execute_script(
            "return arguments[0].scrollHeight;", element
        )

        # Scroll down inside the element multiple times
        for _ in range(num_scrolls):
            # Scroll down inside the element
            driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight);", element
            )

            # Wait to load more content
            time.sleep(scroll_pause_time)

            # Calculate new scroll height after scrolling
            new_height = driver.execute_script(
                "return arguments[0].scrollHeight;", element
            )

            # Break if no more content is loaded
            if new_height == last_height:
                break

            # Update last scroll height
            last_height = new_height

    except Exception as e:
        print(f"Error while scrolling down inside the element: {str(e)}")
        return False

    return True
