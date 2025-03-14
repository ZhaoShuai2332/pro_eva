from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_recommendation_list(driver):
    """
    获取 Recommend 页面中的所有推荐菜品名称
    """
    # 启动 Chrome 浏览器
    # driver = webdriver.Chrome()

    try:
        # **Step 1: 访问推荐页面**
        driver.get("http://localhost:8080/recommend")
        time.sleep(2)  # 等待页面加载

        # **Step 2: 获取所有推荐菜品的名称**
        dish_titles = driver.find_elements(By.CSS_SELECTOR, ".card-title")  # Vue 代码中 h3 使用了 card-title

        # **Step 3: 打印所有菜品名称**
        dish_names = [title.text for title in dish_titles]
        # print("📌 推荐的菜品列表：")
        # for dish in dish_names:
        #     print(f"- {dish}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

    finally:
        # **保持浏览器打开**
        print("✅ 获取完成，浏览器保持打开状态...")
        return driver, dish_names  # 返回 driver 供后续操作

# **调用函数**
# driver = get_recommendation_list()
