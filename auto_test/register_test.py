import requests
import time  # 引入 time 模块

# 创建 API 客户端类
class APIClient:
    def __init__(self, base_url, timeout=5):
        self.session = requests.Session()
        self.base_url = base_url
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        self.timeout = timeout  # 设置默认超时时间

    # 统一的 GET 请求方法
    def get(self, endpoint, params=None):
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=self.timeout)
            response.raise_for_status()  # 抛出 HTTP 错误
            return response.json()
        except requests.exceptions.Timeout:
            print(f"请求超时: {self.base_url}{endpoint}")
        except requests.exceptions.RequestException as e:
            print(f"GET 请求失败: {e}")
        return None

    # 统一的 POST 请求方法
    def post(self, endpoint, data=None):
        try:
            response = self.session.post(f"{self.base_url}{endpoint}", json=data, timeout=self.timeout)
            response.raise_for_status()  # 抛出 HTTP 错误
            return response.json()
        except requests.exceptions.Timeout:
            print(f"请求超时: {self.base_url}{endpoint}")
        except requests.exceptions.RequestException as e:
            print(f"POST 请求失败: {e}")
        return None


# 创建 API 客户端（两个后端）
api = APIClient("http://127.0.0.1:7030", timeout=5)  # 用户注册后端（5秒超时）
api1 = APIClient("http://127.0.0.1:8000", timeout=60)  # 算法后端（15秒超时）

# 注册用户并获取推荐
def register_test(name, email, password, phone, description, img_url, food_type, taste, diet_goal):
    # 1. 发送用户注册请求
    register_data = {
        "userEmail": email,
        "userName": name,
        "userPassword": password,
        "userPhone": phone,
        "userDescription": description,
        "userImg": img_url,
        "isAdmin": False
    }
    register_response = api.post("/register/", register_data)

    if register_response:
        print("✅ 用户注册成功:", register_response)
    else:
        print("❌ 用户注册失败")

    # 2. 等待 20 秒，然后查询饮食推荐
    print("⏳ 深度计算中，等待 20 秒...")

    recommend_params = {
        "userEmail": email,
        "foodPreferences": food_type,
        "tastePreferences": taste,
        "dietGoals": diet_goal
    }
    recommend_response = api1.post("/deepseek_recommend/", recommend_params)

    time.sleep(30)  # 等待 20 秒
    if recommend_response:
        print("✅ 推荐成功:", recommend_response)
    else:
        print("❌ 推荐请求失败")
    
