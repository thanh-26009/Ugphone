import sys
import subprocess

# Hàm kiểm tra và cài đặt thư viện nếu cần
def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Đang cài đặt {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} đã được cài đặt thành công.")

# Tự động cài đặt các thư viện cần thiết
install_package("requests")

# Import các thư viện sau khi đảm bảo chúng đã được cài đặt
import requests
import re
import os

def download_mediafire(url, output_path=None):
    try:
        # Thêm headers để giả lập trình duyệt
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Không thể truy cập URL: {response.status_code}")
            return

        html_content = response.text
        download_link = re.search(r'href="(https://download\d+\.mediafire\.com/[^"]+)"', html_content)
        
        if not download_link:
            print("Không tìm thấy link tải trực tiếp. Có thể file yêu cầu xác nhận hoặc bị lỗi.")
            return
        
        direct_url = download_link.group(1)
        print(f"Link tải trực tiếp: {direct_url}")

        # Trích xuất tên file gốc từ direct_url
        filename = direct_url.split('/')[-1]
        # Nếu output_path được cung cấp, chỉ sử dụng nó làm thư mục, giữ tên file gốc
        if output_path:
            # Kiểm tra xem output_path là thư mục hay tên file
            if os.path.isdir(output_path):
                filename = os.path.join(output_path, filename)
            else:
                filename = output_path
        
        print(f"Đang tải file về: {filename}")
        # Tải file với headers
        file_response = requests.get(direct_url, stream=True, headers=headers)
        
        if file_response.status_code == 200:
            # Đảm bảo thư mục đích tồn tại nếu output_path là thư mục
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            with open(filename, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Tải file thành công: {filename}")
            print("Tải về hoàn tất!")  # Thông báo tải về hoàn tất
        else:
            print(f"Lỗi khi tải file: {file_response.status_code}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    # Kiểm tra xem có tham số dòng lệnh nào được cung cấp không
    if len(sys.argv) < 2:
        print("Vui lòng cung cấp URL MediaFire sau lệnh!")
        print("Ví dụ: python script.py https://www.mediafire.com/file/abc123/example.zip")
        sys.exit(1)
    
    # Lấy URL từ tham số dòng lệnh
    mediafire_url = sys.argv[1]
    output_file = None  # Để None để giữ tên gốc, hoặc chỉ định thư mục/thay tên nếu cần
    download_mediafire(mediafire_url, output_file)