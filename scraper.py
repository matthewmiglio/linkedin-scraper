import os
import random
import time
from re import L

from selenium.webdriver.firefox.webdriver import WebDriver

from firefox import *

TAKE_IT_EASY = True
TAKE_IT_EASY_TIMEOUT = 30

def check_for_linkedin_home_page(driver):
    xpaths = [
        "/html/body/div[6]/div[3]/div/div/div[2]/div/div/div/div/div[1]/div[1]/a[1]/div[2]",
    ]

    texts = get_text_from_xpaths(driver, xpaths)

    for text in texts:
        if "Welcome," in text:
            return True

    return False


def wait_for_linkedin_home_page(driver):
    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_for_linkedin_home_page(driver):
            return True

    return False


def login_to_linkedin(driver, username, password):
    start_time = time.time()

    try:
        driver.get("https://www.linkedin.com/feed/")
    except:
        return False

    username_xpaths = [
        '//*[@id="username"]',
        "/html/body/div/main/div[2]/div[1]/form/div[1]",
        "/html/body/div/main/div[2]/div[1]/form/div[1]/label",
    ]
    password_xpaths = [
        '//*[@id="password"]',
        "/html/body/div/main/div[2]/div[1]/form/div[2]/label",
        "/html/body/div/main/div[2]/div[1]/form/div[2]",
    ]
    sign_in_button_xpaths = [
        "/html/body/div/main/div[2]/div[1]/form/div[4]/button",
        "/html/body/div/main/div[2]/div[1]/form/div[4]",
    ]

    if send_keys(driver, username_xpaths, username) is False:
        print("Fail login! Failed to send username keys")
        return False
    if send_keys(driver, password_xpaths, password) is False:
        print("Fail login! Failed to send username keys")
        return False
    if click_xpaths(driver, sign_in_button_xpaths) is False:
        print("Fail login! Failed to send username keys")
        return False

    if wait_for_linkedin_home_page(driver) is False:
        print("Failed to login to linkedin! Homepage never appeared!")
        input("input here")
        return False

    time_taken = round((time.time() - start_time), 2)
    print(f"Logged in in {time_taken}s")

    return True


def make_search_url(
    search_string, easy_apply=True, experience_level="Internship", start_index=0
):
    # define base url
    base_url = "https://www.linkedin.com/jobs/search/?"

    # add easy apply stuff
    if easy_apply:
        base_url += "f_AL=true&"

    # add keywords stuff
    if search_string is not None:
        keywords = search_string.split(" ")
        keywords_string = "keywords="
        for keyword in keywords:
            keyword = keyword.strip()
            keywords_string += keyword + "%20"
        keywords_string = keywords_string[:-3]
        base_url += keywords_string

    # add experience level stuff
    experience_level_strings_to_index = {
        "Internship": 1,
        "Entry Level": 2,
        "Associate": 3,
        "Mid-Senior Level": 4,
        "Director": 5,
        "Executive": 6,
    }
    if experience_level is not None:
        base_url += f"&f_E={experience_level_strings_to_index[experience_level]}"

    base_url += f"&start={start_index}"

    return base_url


def scrape_job_urls_from_job_search_page(driver):
    urls = []

    for i in range(1000):
        try:
            xpath = f'//*[@id="ember{i}"]'
            element = find_element_by_xpath(driver, xpath)
            href = element.get_attribute("href")

            if "https://www.linkedin.com/jobs" in href:
                urls.append(href)

        except:
            continue

    return urls


def job_search_page_is_loaded(driver):
    xpaths = [
        '//*[@id="navigational-filter_resultType"]',
        '//*[@id="searchFilter_workplaceType"]',
        '//*[@id="ember64"]',
        "/html/body/div[5]/div[4]/aside[1]/div[1]/header/div[2]/button/span/span[1]",
        '//*[@id="compactfooter-copyright"]',
        "/html/body/div[5]/div[3]/div[4]/div/div[2]/main/div/div[2]/div[2]/div/div[2]/div/button",
    ]

    valid_text_keywords = [
        "Jobs",
        "Remote",
        "All filters",
        "LinkedIn Corporation © 2025",
    ]

    texts = get_text_from_xpaths(driver, xpaths)

    for text in texts:
        for valid_text_keyword in valid_text_keywords:
            if valid_text_keyword in text:
                return True

    return False


class Creds:
    def __init__(self):
        self.creds_path = "creds.txt"
        if not os.path.exists(self.creds_path):
            self.make_creds_file()
            print(
                f"No creds file found. Made one at {self.creds_path}.\nPlease fill in the linkedin creds and run again."
            )
            while 1:
                pass

    def make_creds_file(self):
        with open(self.creds_path, "w") as f:
            f.write("username/email:\npassword:")

    def get_creds(self):
        user, password = None, None

        with open(self.creds_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "username/email" in line:
                    user = line.split(":")[1].strip()
                elif "password" in line:
                    password = line.split(":")[1].strip()

        if self.valid_creds(user, password):
            return user, password
        else:
            return False, False

    def valid_creds(self, username, password):
        for text in [username, password]:
            if text is None:
                return False
            if len(text) < 2:
                return False
            if text in ["", " ", "\n", "\t"]:
                return False

        return True


class Saver:
    def __init__(self):
        self.top_dir = os.getcwd()
        self.scrape_text_file_path = os.path.join(self.top_dir, "urls.txt")
        if not os.path.exists(self.scrape_text_file_path):
            self.make_scrape_file()

    def make_scrape_file(self):
        with open(self.scrape_text_file_path, "w") as f:
            f.write("")

    def add_url_to_scrape_file(self, url):
        with open(self.scrape_text_file_path, "a") as f:
            f.write(url + ",")

    def get_saved_urls(self):
        with open(self.scrape_text_file_path, "r") as f:
            urls = f.read().split(",")
            urls = [url for url in urls if len(url) > 1]
        return urls

    def url_is_unique(self, new_url):
        return new_url not in self.get_saved_urls()


class Scraper:
    def __init__(self, search_strings, experience_levels, driver):
        self.driver = driver
        self.search_strings = search_strings
        self.experience_levels = experience_levels
        self.start_index = 0

        # holding current search string stuff
        self.current_search_string = self.search_strings[0]
        self.current_search_string_index = 0
        self.current_experience_level = self.experience_levels[0]
        self.current_experience_index = 0

        # holding results
        self.scraped_urls = []

        # saving results
        self.saver = Saver()

        # credential manager
        cred_manager = Creds()
        self.username, self.password = cred_manager.get_creds()
        if False in [self.username, self.password]:
            print("Invalid creds. Please fill in the creds file and run again.")
            while 1:
                pass

        # login before doing any other operations
        self.do_login()

    def do_login(self):
        while 1:
            if login_to_linkedin(self.driver, self.username, self.password):
                return True
            driver = None
            time.sleep(30)
            driver = make_firefox_driver()

    def make_next_url(self, previous_search_yielded_results: bool):
        # if we got something, just increment the search index
        if previous_search_yielded_results:
            self.start_index += 10

        # else reset the search entirely
        else:
            self.start_index = 0
            self.current_search_string_index = random.randint(
                0, len(self.search_strings) - 1
            )
            self.current_experience_index = random.randint(
                0, len(self.experience_levels) - 1
            )

        # compile new url
        url = make_search_url(
            self.search_strings[self.current_search_string_index],
            True,
            self.experience_levels[self.current_experience_index],
            self.start_index,
        )
        return url

    def locate_scrollable_job_element(self):
        xpaths = [
            "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div",
            "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div",
        ]
        for xpath in xpaths:
            try:
                return find_element_by_xpath(self.driver, xpath)
            except:
                pass

        input("Failed to locate scrollable element. Want to try to find it yourself?")
        return False

    def check_for_no_results_job_search_page(self):
        xpaths = [
            "/html/body/div[6]/div[3]/div[4]/div/div[1]/div/p",
        ]

        valid_text = "No matching jobs found."

        texts = get_text_from_xpaths(self.driver, xpaths)

        for text in texts:
            if valid_text in text:
                return True

        return False

    def check_for_loaded_job_results_page(self):

        xpaths = [
            "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[2]/div/div/div[1]/ul/li[2]/span",
            "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[2]/div/div/div[1]/ul/li[3]/span",
            "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[1]/div/div/div[1]/ul/li[3]/span",
            "/html/body/div[6]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div/ul/li[1]/div/div/div[1]/ul/li[2]/span",
        ]

        for text in get_text_from_xpaths(self.driver, xpaths):
            if "Easy Apply" in text:
                return True

        return False

    def wait_for_job_search_page(self):
        timeout = 10  # s
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_for_no_results_job_search_page():
                return False

            if self.check_for_loaded_job_results_page():
                return True

        return False

    def load_job_page(self) -> bool:
        scrollable_element = self.locate_scrollable_job_element()
        if scrollable_element is False:
            return False
        if (
            scroll_down_inside_element(
                self.driver, scrollable_element, scroll_pause_time=1, num_scrolls=10
            )
            is False
        ):
            print("Failed to load this job page via scrolling!")
            return False

        return True

    def get_to_job_search_page(self, url):
        try:
            self.driver.get(url)
        except:
            return False

        if self.wait_for_job_search_page() is False:
            return False
        if self.load_job_page() is False:
            print(f"Failed somewhere loading this job results page!")
            return False

        return True

    def run(self):
        start_time = time.time()
        these_results = []
        while 1:
            if TAKE_IT_EASY:
                time.sleep(TAKE_IT_EASY_TIMEOUT)
            url = self.make_next_url(len(these_results) > 0)
            if self.get_to_job_search_page(url) is False:
                these_results = []
                continue

            these_results = scrape_job_urls_from_job_search_page(self.driver)
            self.scraped_urls += these_results

            # save these results
            new_urls = 0
            for url in these_results:
                if self.saver.url_is_unique(url):
                    self.saver.add_url_to_scrape_file(url)
                    new_urls += 1

            print(
                f"Scraped {len(these_results)} urls ({new_urls} new) for a total of {len(self.scraped_urls)} this session and {len(self.saver.get_saved_urls())} total in {int(time.time() - start_time)}s"
                + " " * 40,
                end="\r",
            )


class MultithreadScraper:
    def __init__(self, search_strings, experience_levels, thread_count=2):
        self.drivers = [make_firefox_driver() for _ in range(thread_count)]
        self.search_strings = search_strings
        self.experience_levels = experience_levels

    def run(self):
        import threading

        for driver in self.drivers:
            this_scraper = Scraper(self.search_strings, self.experience_levels, driver)
            thread = threading.Thread(target=this_scraper.run, args=())
            thread.start()


def main():
    search_strings = [
        "python developer",
        "python programmer",
        "computer vision engineer",
        "computer vision developer",
        "machine learning engineer",
        "machine learning developer",
        "AI engineer",
        "artificial intelligence engineer",
        "AI/ML engineer",
        "deep learning engineer",
        "data scientist",
        "software engineer",
        "software developer",
        "backend developer",
        "full stack developer",
        "cloud developer",
        "cloud engineer",
        "AWS developer",
        "AWS engineer",
        "serverless application developer",
        "serverless engineer",
        "computer science graduate",
        "entry-level software engineer",
        "entry-level data scientist",
        "entry-level machine learning engineer",
        "entry-level Python developer",
        "big data engineer",
        "big data developer",
        "DevOps engineer",
        "DevOps developer",
        "data pipeline engineer",
        "ETL developer",
        "automation engineer",
        "automation developer",
        "AI researcher",
        "AI scientist",
        "image processing engineer",
        "cloud application developer",
        "AWS specialist",
        "cloud computing engineer",
        "Python and AWS developer",
        "entry-level cloud engineer",
        "entry-level AI engineer",
        "cloud infrastructure engineer",
        "Python automation developer",
        "backend Python developer",
        "AI/ML researcher",
        "entry-level AI/ML researcher",
        "deep learning researcher",
        "natural language processing engineer",
        "real-time AI developer",
        "artificial intelligence architect",
    ]

    experience_levels = [
        None,
        "Internship",
        "Entry Level",
    ]

    scraper = Scraper(search_strings, experience_levels, make_firefox_driver())
    # scraper = MultithreadScraper(search_strings, experience_levels, thread_count=3)
    scraper.run()


if __name__ == "__main__":
    main()
