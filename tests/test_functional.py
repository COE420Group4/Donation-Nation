from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

class TestFunctional():
	def setup_method(self, method):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		self.driver = webdriver.Chrome(options=chrome_options)
		self.vars = {}

	def teardown_method(self, method):
		self.driver.quit()

	def test_userRemoveItem(self):
		pass

	def test_orgRejectItem(self):
		pass

	def test_userAcceptPickupTime(self):
		pass

	def test_orgAcceptPickupTime(self):
		pass

	def test_userRejectPickupTime(self):
		pass

	def test_orgRejectPickupTime(self):
		pass

	# * This also includes checking if we can access the other account's info
	def test_userViewMore(self):
		pass

	def test_orgViewMore(self):
		pass

	def test_adminRejectOrg(self):
		pass

	def test_adminAcceptOrg(self):
		pass