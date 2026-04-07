from langchain_core.tools import tool

# ============================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# ============================================================
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    """
    flights = FLIGHTS_DB.get((origin, destination))
    
    # Thử tra ngược nếu không có
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."
    
    result = f"Danh sách chuyến bay giữa {origin} và {destination}:\n"
    for f in flights:
        price_str = f"{f['price']:,}".replace(",", ".") + "đ"
        result += f"- {f['airline']} ({f['class']}): {f['departure']} -> {f['arrival']}, Giá: {price_str}\n"
    return result

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    """
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}."
    
    # Lọc theo giá
    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    
    if not filtered_hotels:
        price_str = f"{max_price_per_night:,}".replace(",", ".") + "đ"
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {price_str}/đêm. Hãy thử tăng ngân sách."
    
    # Sắp xếp theo rating giảm dần
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)
    
    result = f"Danh sách khách sạn tại {city} (Giá tối đa {max_price_per_night:,}đ/đêm):\n".replace(",", ".")
    for h in filtered_hotels:
        price_str = f"{h['price_per_night']:,}".replace(",", ".") + "đ"
        result += f"- {h['name']} ({h['stars']} sao) - {h['area']}. Rating: {h['rating']}. Giá: {price_str}/đêm\n"
    return result

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, định dạng 'tên_khoản:số_tiền' cách nhau bởi dấu phẩy
    VD: 'vé_máy_bay:890000,khách_sạn:650000'
    """
    try:
        # Parse chuỗi expenses
        expense_items = [item.strip() for item in expenses.split(',')]
        expense_dict = {}
        total_expense = 0
        
        for item in expense_items:
            name, amount_str = item.split(':')
            amount = int(amount_str.strip())
            expense_dict[name.strip()] = amount
            total_expense += amount
            
        remaining = total_budget - total_expense
        
        # Format kết quả
        result = "Bảng chi phí:\n"
        for name, amount in expense_dict.items():
            result += f"- {name.capitalize().replace('_', ' ')}: {amount:,}đ\n".replace(",", ".")
        result += "---\n"
        result += f"Tổng chi: {total_expense:,}đ\n".replace(",", ".")
        result += f"Ngân sách: {total_budget:,}đ\n".replace(",", ".")
        result += f"Còn lại: {remaining:,}đ\n".replace(",", ".")
        
        if remaining < 0:
            result += f"\nVượt ngân sách {abs(remaining):,}đ! Cần điều chỉnh.".replace(",", ".")
            
        return result
        
    except Exception as e:
        return f"Lỗi định dạng expenses. Hãy đảm bảo định dạng là 'tên:số_tiền,tên:số_tiền'. Chi tiết lỗi: {str(e)}"