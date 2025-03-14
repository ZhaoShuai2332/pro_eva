from auto_test.login_test import login_test
from auto_test.register_test import register_test
from auto_test.recommend_test import get_recommendation_list
from auto_test.purchase_test import purchase_test
from auto_test.collect_test import collect_test

# driver = login_test("admin@admin.com", "admin123")

# driver = collect_test(driver, "Oyster scrambled eggs", action="collect")

# driver, disher_names = get_recommendation_list(driver)

# **示例调用**
# driver = register_test(
#     name="TestUser",
#     email="testuser@example5.com",
#     password="Test@1234",
#     phone="1234567890",
#     description="This is a test user",
#     img_url="https://via.placeholder.com/150",
#     food_type=["Chinese Cuisine"],  # **可以多选或单选**
#     taste=["Spicy & Numbing"],  # **可以多选或单选**
#     diet_goal="Healthy Eating"  # **单选**
# )
