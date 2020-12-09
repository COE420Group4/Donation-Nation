import pytest
import time
import json
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

# * This is a suite of tests to test functionality that relates to the GUI (alerts exists, buttons are clickable, etc)

class TestGUI():
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

	# * User login
	def test_user_valid_credentials(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		assert 'Dashboard' in self.driver.title

	def test_user_invalid_credentials(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").click()
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("b")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		assert 'Dashboard' not in self.driver.title

	def test_user_logout(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
		self.driver.find_element(By.ID, "logoutButton").click()
		elements = self.driver.find_elements(By.CSS_SELECTOR, ".alert")
		assert len(elements) > 0

	# * Org login
	def test_org_valid_credentials(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(2) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("contact@redcrescent.org")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
		assert "Dashboard" in self.driver.title

	def test_org_invalid_credentials(self):
			self.driver.get("http://127.0.0.1:5000/")
			self.driver.set_window_size(1200, 1000)
			self.driver.find_element(By.ID, "loginButton").click()
			self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(2) .img-fluid").click()
			self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("contact@redcrescent.org")
			self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("b")
			self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
			assert "Dashboard" not in self.driver.title

	def test_org_logout(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(2) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("contact@redcrescent.org")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
		self.driver.find_element(By.ID, "logoutButton").click()
		elements = self.driver.find_elements(By.CSS_SELECTOR, ".alert")
		assert len(elements) > 0

	# * Viewing own profiles
	def test_user_view_profile(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("rich@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
		self.driver.find_element(By.LINK_TEXT, "View Profile").click()
		assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) > .col:nth-child(1) > p").text == "Richy"

	def test_org_view_profile(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(2) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("contact@dubaicares.org")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
		self.driver.find_element(By.LINK_TEXT, "View Profile").click()
		assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) > .col:nth-child(1) > p").text == "Dubai Cares"

	# * Test listing organization
	def test_viewOrganizationProfileAsUser(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
		self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(2) > .col-md-4:nth-child(4) > .btn").click()
		self.driver.find_element(By.LINK_TEXT, "View Profile").click()
		assert self.driver.find_element(By.CSS_SELECTOR, ".display-1").text == "Red Crescent"

	def test_viewOrganizationProfileLoggedOut(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.LINK_TEXT, "Organizations").click()
		self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(3) .btn").click()
		assert self.driver.find_element(By.CSS_SELECTOR, ".display-1").text == "UAE Aid"

	# * Test editing own information
	def test_testUserChangingInfo(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1053)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("jake@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		self.driver.find_element(By.LINK_TEXT, "View Profile").click()
		self.driver.find_element(By.LINK_TEXT, "Edit Profile").click()
		WebDriverWait(self.driver, 30000).until(expected_conditions.element_to_be_clickable((By.ID, "validationTooltip04")))
		self.driver.find_element(By.ID, "validationTooltip04").click()
		dropdown = self.driver.find_element(By.ID, "validationTooltip04")
		dropdown.find_element(By.XPATH, "//option[. = 'Dubai']").click()
		element = self.driver.find_element(By.ID, "PO-BOX")
		actions = ActionChains(self.driver)
		actions.double_click(element).perform()
		self.driver.find_element(By.ID, "PO-BOX").send_keys("990099")
		self.driver.find_element(By.CSS_SELECTOR, "#edit .btn-primary").click()
		assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(8) > .col:nth-child(3) > p").text == "990099"

	# ! These should always be last!
	def test_testOrgChangingPassword(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(2) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("contact@redcrescent.org")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		self.driver.find_element(By.LINK_TEXT, "View Profile").click()
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(1)").click()
		WebDriverWait(self.driver, 30000).until(expected_conditions.element_to_be_clickable((By.ID, "validationTooltip07")))
		self.driver.find_element(By.ID, "validationTooltip07").send_keys("b")
		self.driver.find_element(By.ID, "validationTooltip08").send_keys("b")
		self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(2)").click()
		self.driver.find_element(By.ID, "logoutButton").click()
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(2) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("contact@redcrescent.org")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("b")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		assert self.driver.find_element(By.ID, "intro").text == "Hello, Red Crescent!"

	def test_testUserChangingPassword(self):
		self.driver.get("http://127.0.0.1:5000/")
		self.driver.set_window_size(1200, 1000)
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		self.driver.find_element(By.LINK_TEXT, "View Profile").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-md-12 > .btn:nth-child(2)").click()
		WebDriverWait(self.driver, 30000).until(expected_conditions.element_to_be_clickable((By.ID, "validationTooltip07")))
		self.driver.find_element(By.ID, "validationTooltip07").send_keys("b")
		self.driver.find_element(By.ID, "validationTooltip08").send_keys("b")
		self.driver.find_element(By.CSS_SELECTOR, "#changePassword .btn-primary").click()
		self.driver.find_element(By.ID, "logoutButton").click()
		self.driver.find_element(By.ID, "loginButton").click()
		self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
		self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
		self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("b")
		self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
		self.driver.find_element(By.ID, "intro").click()
		assert self.driver.find_element(By.ID, "intro").text == "Hello, Donald!"