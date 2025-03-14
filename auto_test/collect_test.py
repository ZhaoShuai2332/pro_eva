from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import time

def collect_test(driver, dish_name, action="collect"):
    """
    根据菜品名称选择商品并进行操作
    :param driver: 已登录的 WebDriver
    :param dish_name: 要选择的菜品名称（如 "Sweet and Sour Ribs"）
    :param action: 操作类型 ("collect" or "purchase")
    """
    try:
        # **Step 1: 查找所有菜品卡片**
        dish_cards = driver.find_elements(By.CSS_SELECTOR, "div.card")

        for card in dish_cards:
            # **Step 2: 查找菜品名称**
            title_element = card.find_element(By.TAG_NAME, "h3")  # 可能需要调整为实际的标签
            if dish_name.lower() in title_element.text.lower():
                print(f"✅ 找到菜品: {title_element.text}")

                # **滚动到该商品**
                driver.execute_script("arguments[0].scrollIntoView();", card)
                time.sleep(1)  # 等待滚动完成

                # **Step 3: 根据操作类型点击按钮**
                if action == "collect":
                    button = card.find_element(By.XPATH, ".//button[contains(text(), 'Collect')]")
                    button.click()
                    print(f"✅ 已收藏: {dish_name}")

                    # **处理收藏成功的 alert 弹窗**
                    time.sleep(1)
                    try:
                        alert = driver.switch_to.alert
                        print("弹窗信息:", alert.text)
                        alert.accept()  # 点击“确定”
                        print("✅ 收藏成功，弹窗已关闭")
                    except NoAlertPresentException:
                        print("❌ 没有检测到收藏成功的弹窗")

                elif action == "purchase":
                    button = card.find_element(By.XPATH, ".//button[contains(text(), 'Purchase')]")
                    button.click()
                    print(f"✅ 已购买: {dish_name}")

                    # **处理购买成功的 alert 弹窗**
                    time.sleep(1)
                    try:
                        alert = driver.switch_to.alert
                        print("弹窗信息:", alert.text)
                        alert.accept()  # 点击“确定”
                        print("✅ 购买成功，弹窗已关闭")
                    except NoAlertPresentException:
                        print("❌ 没有检测到购买成功的弹窗")

                else:
                    print("❌ 无效的操作类型！")
                return

        print(f"❌ 未找到菜品: {dish_name}")

    except NoSuchElementException as e:
        print(f"❌ 发生错误: {e}")