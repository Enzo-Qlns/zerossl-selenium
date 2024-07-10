import os
import time
import uuid
import shutil
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import utils
from config import settings


class ZeroSSLService:
    _path_image = None
    _excel_filename = "certificates.xlsx"
    _driver = None

    def __init__(self) -> None:
        """
        Initialize the ZeroSSLService class
        """
        download_dir = os.path.abspath("static")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')

        if utils.is_dev():
            self._driver = webdriver.Chrome(options=options)
        else:
            self._driver = webdriver.Remote(
                command_executor='http://zerossl-selenium-chrome:4444',
                options=options
            )

        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        self.wait = WebDriverWait(self._driver, 300)
        self.create_excel_if_not_exists()

    @staticmethod
    def sleep(seconds) -> None:
        """
        Sleep for a specified number of seconds
        :param seconds:
        :return:
        """
        time.sleep(seconds)

    def click_element(self, by, value) -> None:
        """
        Click an element on the page by the specified locator
        :param by:
        :param value:
        :return:
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.sleep(1)  # wait for the scroll action to complete
            element.click()
            self.sleep(2)
        except (TimeoutException, ElementClickInterceptedException) as e:
            self._driver.save_screenshot('error.png')
            print(f"Error clicking element: {value}. Screenshot saved as error.png")
            raise e

    def send_keys_element(self, by, value, keys) -> None:
        """
        Send keys to an element on the page by the specified locator
        :param by:
        :param value:
        :param keys:
        :return:
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.sleep(1)  # wait for the scroll action to complete
            element.send_keys(keys)
            self.sleep(2)
        except TimeoutException as e:
            self._driver.save_screenshot('error.png')
            print(f"Error sending keys to element: {value}. Screenshot saved as error.png")
            raise e

    def get_cert(self, to_email, random_email, domain) -> None:
        """
        Get a certificate from ZeroSSL for the specified domain
        :param to_email:
        :param random_email:
        :param domain:
        :return:
        """
        self._driver.get("https://zerossl.com/")
        self._driver.set_window_size(1512, 944)

        self.click_element(By.CSS_SELECTOR, ".login > a")
        self.click_element(By.LINK_TEXT, "Get started for free")
        self.send_keys_element(By.NAME, "signup[email]", random_email)
        self.send_keys_element(By.NAME, "signup[password]", settings.PASSWORD)
        self.click_element(By.CSS_SELECTOR, ".button")
        self.click_element(By.LINK_TEXT, "New Certificate")
        self.send_keys_element(By.NAME, "wizard[order][domains][domain]", domain)
        self.click_element(By.LINK_TEXT, "Next Step")
        self.click_element(By.CSS_SELECTOR, ".radio:nth-child(2) span")
        self.click_element(By.LINK_TEXT, "Next Step")
        self.click_element(By.LINK_TEXT, "Next Step")
        self.click_element(By.LINK_TEXT, "Next Step")
        self.click_element(By.LINK_TEXT, "Next Step")
        self.click_element(By.ID, "wizard[validate][method][email][selected_email]")

        dropdown = self.wait.until(
            EC.presence_of_element_located((By.ID, "wizard[validate][method][email][selected_email]")))
        dropdown.find_element(By.XPATH, f"//option[. = '{to_email}']").click()
        self.sleep(2)

        self.click_element(By.LINK_TEXT, "Next Step")
        self.click_element(By.LINK_TEXT, "Verify Domain")

        while True:
            try:
                self._driver.find_element(By.LINK_TEXT, "Install Certificate")
                break
            except NoSuchElementException:
                self.click_element(By.LINK_TEXT, "Refresh Status")
                self.sleep(5)

        self.click_element(By.LINK_TEXT, "Install Certificate")
        self.click_element(By.LINK_TEXT, "Download Certificate (.zip)")

        # Wait for the download to complete
        self.sleep(10)

        # Move the downloaded file to the desired location with a unique UUID name
        download_dir = os.path.abspath("static")
        for filename in os.listdir(download_dir):
            if filename.endswith(".zip"):
                unique_filename = f"{domain}-{uuid.uuid4()}.zip"
                source = os.path.join(download_dir, filename)
                destination = os.path.join(download_dir, unique_filename)
                shutil.move(source, destination)
                self._path_image = utils.get_api_url() + '/static/' + unique_filename
                # Add certificate details to Excel
                self.add_to_excel(unique_filename, domain)

    def create_excel_if_not_exists(self) -> None:
        """
        Create the Excel file if it does not exist
        :return:
        """
        if not os.path.exists(self._excel_filename):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Certificates"
            sheet.append(["File Name", "Domain"])
            workbook.save(self._excel_filename)

    def add_to_excel(self, filename, domain) -> None:
        """
        Add the certificate details to the Excel file
        :param filename:
        :param domain:
        :return:
        """
        workbook = openpyxl.load_workbook(self._excel_filename)
        sheet = workbook.active
        sheet.append([filename, domain])
        workbook.save(self._excel_filename)

    def get_path_image(self) -> str:
        """
        Get the path to the downloaded certificate
        :return:
        """
        return self._path_image

    def close(self) -> None:
        """
        Close the browser and quit the driver instance
        :return:
        """
        self._driver.quit()
