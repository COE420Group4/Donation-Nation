# Generated by Selenium IDE
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

class TestUserProfile():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()

  def test_view_profile(self):
    self.driver.get("http://127.0.0.1:5000/")
    self.driver.set_window_size(800, 600)
    self.driver.find_element(By.ID, "loginButton").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
    self.driver.find_element(By.ID, "exampleInputEmail1").click()
    self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
    self.driver.find_element(By.ID, "exampleInputPassword1").click()
    self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
    self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
    self.driver.find_element(By.LINK_TEXT, "View Profile").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) > .col:nth-child(1) > p").text == "Donald"
