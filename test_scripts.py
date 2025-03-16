from auto_test.login_test import login_test
from auto_test.register_test import register_test
from auto_test.recommend_test import get_recommendation_list
from auto_test.purchase_test import purchase_test
from auto_test.collect_test import collect_test
from auto_test.wishlist_test import get_wishlist
from auto_test.deepseek_test import generate_prompt, extract_json_data, chat_with_ai, parse_json_string, calculate_precision_coverage
import json
import pandas as pd
import time

# 读取 Excel 文件
file_path = r"D:\projects\admin_sys\pro_eva\auto_test\user_info.xlsx"
df = pd.read_excel(file_path)

def get_clicks_purchases():
    Clicks = 0
    Purchases = 0
    Recommend_list = []
    Wish_list = []
    for index, row in df.iterrows():
        email = row["email"]
        password = row["password"]
        driver = login_test(email, password)
        driver, recommend_list = get_recommendation_list(driver)
        driver, wish_list = get_wishlist(driver)
        driver.quit()
        response = chat_with_ai(generate_prompt(recommend_list, wish_list))
        print(response)
        data = extract_json_data(response)
        clicks = data["Click_Count"]
        purchases = data["Purchase_Count"]
        Clicks += clicks
        Purchases += purchases
        Recommend_list.append(recommend_list)
        Wish_list.append(wish_list)
        print(f"User {email} has {clicks} clicks and {purchases} purchases.")
        print(f"Current Total Clicks: {Clicks}, Current Total Purchases: {Purchases}")
        time.sleep(3)
    return Clicks, Purchases, Recommend_list, Wish_list

if __name__ == "__main__":
    for i in range(5):
        clicks, purchases, recommend_list, wish_list = get_clicks_purchases()
        cvr = purchases / clicks
        precision, coverage = calculate_precision_coverage(recommend_list, wish_list)
        print(f"Precision: {precision}, Coverage: {coverage}")
        print(f"Total Clicks: {clicks}, Total Purchases: {purchases}, Total CVR: {cvr}")
        with open("res.txt", "a") as file:
            file.write(f"Total Clicks: {clicks}, Total Purchases: {purchases}, Total CVR: {cvr}\n")
            file.write(f"Precision: {precision}, Coverage: {coverage}\n")
        time.sleep(5)

