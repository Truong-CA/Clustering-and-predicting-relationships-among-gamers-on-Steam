import pandas as pd
import ast # Thư viện để xử lý các chuỗi ký tự

def find_top_group_members(csv_file_path, top_n=10):
    """
    Đọc file CSV, đếm số lượng nhóm mà mỗi người dùng tham gia, và in ra top N người dùng.
    """
    print(f"Bắt đầu phân tích file: {csv_file_path} để tìm người dùng hàng đầu...")
    try:
        # Sử dụng encoding='utf-8' để đọc file an toàn hơn
        df = pd.read_csv(csv_file_path, encoding='utf-8')
    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file CSV tại đường dẫn: '{csv_file_path}'")
        return
    except UnicodeDecodeError:
        print("❌ Lỗi: Lỗi giải mã Unicode. Hãy đảm bảo file CSV được lưu dưới định dạng UTF-8.")
        return
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi đọc file: {e}")
        return

    # 1. Đảm bảo cột GID tồn tại
    gid_column = 'all_groups_gid'
    if gid_column not in df.columns:
        print(f"❌ Lỗi: Không tìm thấy cột '{gid_column}' trong file.")
        return
    
    # 2. Định nghĩa hàm đếm số nhóm cho mỗi người dùng
    def count_groups(gid_string):
        """Đếm số GID trong một chuỗi, phân tách bằng '|'"""
        if pd.isna(gid_string) or not gid_string:
            return 0
        
        # Tách chuỗi và loại bỏ các chuỗi rỗng sau khi tách
        gids = [gid.strip() for gid in str(gid_string).split('|') if gid.strip()]
        return len(gids)

    # 3. Áp dụng hàm đếm lên cột và tạo cột mới 'group_count'
    print("Đang đếm số lượng nhóm cho từng người dùng...")
    df['group_count'] = df[gid_column].apply(count_groups)

    # 4. Sắp xếp và lấy top N
    top_users = df.sort_values(by='group_count', ascending=False).head(top_n)

    # 5. In kết quả
    print("\n=======================================================")
    print(f"🥇 TOP {top_n} NGƯỜI DÙNG CÓ NHIỀU NHÓM NHẤT")
    print("=======================================================")
    
    # Giả sử file CSV của bạn có cột 'steamid' hoặc 'profile_url' để xác định người dùng
    # Nếu không có, bạn có thể thay thế bằng index của DataFrame (df.index)
    if 'steamid' in df.columns:
        user_id_column = 'steamid'
    elif 'profile_url' in df.columns:
        user_id_column = 'profile_url'
    else:
        user_id_column = df.columns[0] # Lấy cột đầu tiên làm ID tạm thời
        print(f"⚠️ Không tìm thấy cột 'steamid' hoặc 'profile_url'. Sử dụng cột '{user_id_column}' làm ID.")

    for index, row in top_users.iterrows():
        print(f"Người dùng ID: {row[user_id_column]:<30} | Số nhóm: {row['group_count']}")

# --- THÔNG SỐ CẦN THAY ĐỔI ---
INPUT_CSV = 'data_users.csv' # ⚠️ Thay bằng tên file CSV gốc của bạn

# Thực thi hàm
find_top_group_members(INPUT_CSV, top_n=10)