import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestApp(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def test_user_login(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Login").click()
        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("testuser")
        password_input.send_keys("testpassword")
        password_input.send_keys(Keys.RETURN)
        tasks_header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2"))).text
        self.assertEqual(tasks_header, "Your tasks")

    def test_incorrect_user_login(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Login").click()
        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("testuser")
        password_input.send_keys("incorrectpassword")
        password_input.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
        alert_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertEqual(alert_message, "Login failed. Check your username and password.")

    def test_add_and_remove_task(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Login").click()
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("testpassword")
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        task_input = driver.find_element(By.NAME, "content")
        task_input.send_keys("Test task")
        task_input.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(lambda d: "Test task\nDelete" in [task.text for task in d.find_elements(By.TAG_NAME, "li")])
        tasks = driver.find_elements(By.TAG_NAME, "li")
        self.assertIn("Test task\nDelete", [task.text for task in tasks])
        delete_link = driver.find_element(By.XPATH, "//li[contains(text(), 'Test task')]//a[text()='Delete']")
        delete_link.click()
        WebDriverWait(driver, 10).until(EC.staleness_of(delete_link))
        tasks = driver.find_elements(By.TAG_NAME, "li")
        self.assertNotIn("Test task\nDelete", [task.text for task in tasks])

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
