from _pytest.config import parse_warning_filter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import sys # ! Don't remove this line.
sys.path.append('.')
from db import DB

# * This is functional testing, this is testing the core functionality of the application
class TestFunctional():
	def setup_method(self, method):
		self.sql = DB()
		self.sql.clear_db()
		self.sql.init_db()
		self.sql.populate()
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		self.driver = webdriver.Chrome(options=chrome_options)
		self.vars = {}

	def teardown_method(self, method):
		self.driver.quit()

	def test_userRemoveItem(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		self.driver.find_element(By.LINK_TEXT, "View Items").click()
		self.driver.find_element(By.CSS_SELECTOR, ".my-3:nth-child(5)").click()
		WebDriverWait(self.driver, 30000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".show[aria-labelledby=\"removeItemLabel\"] form > .btn")))
		self.driver.find_element(By.CSS_SELECTOR, ".show[aria-labelledby=\"removeItemLabel\"] form > .btn").click()
		WebDriverWait(self.driver, 30000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".row:nth-child(1) .card:nth-child(1) .card-title")))
		text = self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) .card:nth-child(1) .card-title").text
		assert text != "Red Shirt"

	def test_orgRejectItem(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(2) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("contact@redcrescent.org")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		self.driver.find_element(By.LINK_TEXT, "View Items").click()
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) .my-3:nth-child(2)").click()
		WebDriverWait(self.driver, 30000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".show[aria-labelledby=\"removeItemLabel\"] form > .btn")))
		self.driver.find_element(By.CSS_SELECTOR, ".show[aria-labelledby=\"removeItemLabel\"] form > .btn").click()
		WebDriverWait(self.driver, 30000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".card:nth-child(1) .card-title")))
		text = self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(1) .card-title").text
		assert text != "Red Hoodie"

	def test_adminRejectOrg(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("admin@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		self.driver.find_element(By.LINK_TEXT, "✗").click()
		text = self.driver.find_element(By.CSS_SELECTOR, "tbody:nth-child(2) td:nth-child(2)").text
		assert text != "Testing Org 1"

	def test_adminAcceptOrg(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("admin@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		self.driver.find_element(By.LINK_TEXT, "✓").click()
		text = self.driver.find_element(By.CSS_SELECTOR, "tbody:nth-child(2) td:nth-child(2)").text
		assert text != "Testing Org 1"