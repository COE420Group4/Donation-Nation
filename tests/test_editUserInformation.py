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

class TestEditUserInformation():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_editUserInformation(self):
    self.driver.get("http://127.0.0.1:5000/")
    self.driver.set_window_size(1552, 840)
    self.driver.find_element(By.ID, "loginButton").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col-4:nth-child(1) .img-fluid").click()
    self.driver.find_element(By.ID, "exampleInputEmail1").click()
    self.driver.find_element(By.ID, "exampleInputEmail1").send_keys("donald@email.com")
    self.driver.find_element(By.ID, "exampleInputPassword1").send_keys("a")
    self.driver.find_element(By.ID, "exampleInputPassword1").send_keys(Keys.ENTER)
    self.driver.find_element(By.LINK_TEXT, "View Profile").click()
    self.driver.find_element(By.LINK_TEXT, "Edit Profile").click()
    self.driver.find_element(By.ID, "validationTooltip03").click()
    self.driver.find_element(By.ID, "edit").click()
    self.driver.find_element(By.ID, "validationTooltip03").send_keys("Kidzania")
    self.driver.find_element(By.ID, "validationTooltip04").click()
    dropdown = self.driver.find_element(By.ID, "validationTooltip04")
    dropdown.find_element(By.XPATH, "//option[. = 'Dubai']").click()
    self.driver.find_element(By.ID, "validationTooltip04").click()
    self.driver.find_element(By.CSS_SELECTOR, ".form-row:nth-child(3)").click()
    self.driver.find_element(By.ID, "PO-BOX").send_keys("44444")
    self.driver.find_element(By.ID, "edit").click()
    self.driver.find_element(By.NAME, "address1").send_keys("Kidzania")
    self.driver.find_element(By.ID, "edit").click()
    self.driver.find_element(By.NAME, "address2").send_keys("In Dubai Mall")
    self.driver.find_element(By.ID, "edit").click()
    self.driver.find_element(By.ID, "validationTooltip05").send_keys(Keys.UP)
    self.driver.find_element(By.ID, "validationTooltip05").send_keys(Keys.UP)
    self.driver.find_element(By.ID, "validationTooltip05").send_keys(Keys.UP)
    self.driver.find_element(By.CSS_SELECTOR, "#edit .btn-primary").click()
    self.driver.find_element(By.CSS_SELECTOR, ".close:nth-child(1) > span").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(8) > .col:nth-child(1) > p").text == "Kidzania"
    assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(9) p").text == "Kidzania"
    assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(10) p").text == "In Dubai Mall"
    assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(8) > .col:nth-child(3) > p").text == "44444"
    assert self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(8) > .col:nth-child(2) > p").text == "Dubai"
  