import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# 載入環境變數
load_dotenv()

class WeatherTracker:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        # 使用 HTTPS 端點
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    def get_weather(self, city="Taipei"):
        """獲取指定城市的天氣信息"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'zh_tw'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            
            # 檢查響應狀態
            if response.status_code == 401:
                return "API 密鑰驗證失敗。請確認：\n1. API 密鑰是否正確\n2. API 密鑰是否已激活（可能需要等待約2小時）\n3. 是否已在 OpenWeatherMap 網站啟用 API 密鑰"
            elif response.status_code == 404:
                return f"找不到城市 '{city}' 的天氣信息"
            elif response.status_code != 200:
                return f"獲取天氣信息時發生錯誤: HTTP {response.status_code}"
                
            data = response.json()
            
            # 提取天氣信息
            weather_info = {
                '城市': data['name'],
                '溫度': f"{data['main']['temp']}°C",
                '體感溫度': f"{data['main']['feels_like']}°C",
                '濕度': f"{data['main']['humidity']}%",
                '天氣狀況': data['weather'][0]['description'],
                '風速': f"{data['wind']['speed']} m/s",
                '更新時間': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            return f"網絡請求錯誤: {str(e)}"
        except Exception as e:
            return f"發生未知錯誤: {str(e)}"
    
    def display_weather(self, weather_info):
        """顯示天氣信息"""
        if isinstance(weather_info, dict):
            print("\n=== 天氣信息 ===")
            for key, value in weather_info.items():
                print(f"{key}: {value}")
        else:
            print(weather_info)

def main():
    tracker = WeatherTracker()
    
    # 預設城市列表
    cities = ['Taipei', 'Kaohsiung', 'Taichung']
    
    print("台灣天氣追蹤器")
    print("=" * 20)
    
    while True:
        print("\n請選擇操作：")
        print("1. 查看預設城市天氣")
        print("2. 輸入城市名稱查詢")
        print("3. 退出")
        
        choice = input("\n請輸入選項 (1-3): ")
        
        if choice == '1':
            for city in cities:
                print(f"\n正在獲取 {city} 的天氣信息...")
                weather_info = tracker.get_weather(city)
                tracker.display_weather(weather_info)
                
        elif choice == '2':
            city = input("請輸入城市名稱（英文）: ")
            print(f"\n正在獲取 {city} 的天氣信息...")
            weather_info = tracker.get_weather(city)
            tracker.display_weather(weather_info)
            
        elif choice == '3':
            print("感謝使用！再見！")
            break
            
        else:
            print("無效的選項，請重新選擇。")

if __name__ == "__main__":
    main() 