from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
import time

def login_test(email, password, keep_open=True, driver=None):
    """
    自动化测试登录功能

    :param email: 用户邮箱
    :param password: 用户密码
    :param keep_open: 是否保持浏览器打开（默认 True）
    :return: WebDriver 对象（如果 keep_open=True）
    """
    # 启动 Chrome 浏览器
    driver = webdriver.Chrome()

    try:
        # 访问登录页面
        driver.get("http://localhost:8080/login")  # 替换为你的实际 URL
        time.sleep(2)

        # 输入邮箱
        email_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Please input email']")
        email_input.send_keys(email)

        # 输入密码
        password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Please input password']")
        password_input.send_keys(password)

        # 勾选用户协议
        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
        checkbox.click()

        # 点击 "Login" 按钮
        login_button = driver.find_element(By.CSS_SELECTOR, "button")
        login_button.click()

        time.sleep(2)  # 等待弹窗出现

        # 处理弹窗
        try:
            alert = driver.switch_to.alert
            print("弹窗信息:", alert.text)  # 打印弹窗内容
            alert.accept()  # 点击“确定”
            print("弹窗已关闭")
        except NoAlertPresentException:
            print("没有检测到弹窗")

        # 等待 1 秒，进入主界面
        time.sleep(1)

        # 跳转到主界面
        driver.get("http://localhost:8080/")  # 替换为主界面 URL
        time.sleep(2)

        print("✅ 登录成功，并已跳转到主界面！")

        if keep_open:
            return driver  # 返回 WebDriver 供后续操作
        else:
            driver.quit()  # 关闭浏览器

    except NoSuchElementException as e:
        print(f"❌ 发生错误：{e}")
        driver.quit()

