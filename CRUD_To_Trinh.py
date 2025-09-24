import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import traceback

# --- HÀM TRỢ GIÚP ĐỂ XỬ LÝ DROPDOWN PHỨC TẠP (NG-SELECT) ---
def handle_custom_dropdown(wait: WebDriverWait, dropdown_name_attribute: str, option_text: str):
    try:
        # 1. Chờ ng-select và click để mở dropdown
        dropdown_locator = (By.CSS_SELECTOR, f"createoredittotrinhmodal ng-select[name='{dropdown_name_attribute}']")
        dropdown = wait.until(EC.element_to_be_clickable(dropdown_locator))
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
        dropdown.click()
        time.sleep(1)

        # 2. Chờ input bên trong ng-select và nhập từ khóa
        input_locator = (By.CSS_SELECTOR, f"createoredittotrinhmodal ng-select[name='{dropdown_name_attribute}'] input[type='text']")
        input_box = wait.until(EC.element_to_be_clickable(input_locator))
        input_box.clear()
        input_box.send_keys(option_text[:8])
        time.sleep(2)

        # 3. Chờ và click phần tử đầu tiên trong danh sách suggest
        first_option_locator = (By.CSS_SELECTOR, "ng-dropdown-panel .ng-option")
        first_option = wait.until(EC.element_to_be_clickable(first_option_locator))
        driver.execute_script("arguments[0].scrollIntoView(true);", first_option)
        first_option.click()
        print(f"Đã chọn phần tử đầu tiên từ dropdown '{dropdown_name_attribute}' thành công.")
        time.sleep(1)
    except TimeoutException:
        print(f"Lỗi: Không tìm thấy dropdown '{dropdown_name_attribute}' hoặc danh sách suggest.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi xử lý dropdown '{dropdown_name_attribute}': {e}")

def delay_step(seconds=2):
    print(f"Đang chờ {seconds} giây giữa các bước...")
    time.sleep(seconds)

# --- KHỞI TẠO TRÌNH DUYỆT ---
driver = webdriver.Chrome()  # không cần chỉ đường dẫn
driver.maximize_window()

# URL của trang đích, hệ thống thường sẽ tự chuyển đến trang đăng nhập nếu chưa có phiên làm việc
driver.get("http://barter.test.dwh.admicro/app/main/appToTrinh/toTrinh") 

wait = WebDriverWait(driver, 15) # Tăng thời gian chờ lên 15s cho chắc chắn

try:
    # --- BƯỚC 1: ĐĂNG NHẬP ---
    print("Chờ trang đăng nhập tải...")
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "userNameOrEmailAddress")))
    delay_step()
    print("Bắt đầu điền thông tin đăng nhập...")
    # THAY THÔNG TIN ĐĂNG NHẬP CỦA BẠN VÀO ĐÂY
    username_field.send_keys("thuyduongnguyen") 
    driver.find_element(By.NAME, "password").send_keys("123qwe")
    
    # Tìm và nhấn nút đăng nhập (Giả định nút có text là 'Đăng nhập')
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Log in')]")))
    login_button.click()
    print("Đã gửi thông tin đăng nhập.")
    delay_step()

    # --- BƯỚC 2: MỞ FORM THÊM MỚI ---
    print("Đăng nhập thành công. Chờ trang danh sách tờ trình tải...")
    # Chờ cho nút "Thêm tờ trình" sẵn sàng để click, đây là dấu hiệu đăng nhập thành công
    add_button_locator = (By.XPATH, "//button[normalize-space()='Thêm tờ trình']")
    add_button = wait.until(EC.element_to_be_clickable(add_button_locator))
    print("Trang danh sách đã tải. Click nút 'Thêm tờ trình'...")
    add_button.click()
    print("Đã click nút 'Thêm tờ trình'. Chờ form hiện ra...")
    delay_step()

    # Chờ cho một phần tử đặc trưng của form, ví dụ ô 'Người đề xuất'
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ng-select[name='nguoiDeXuat_Ref'] input[type='text']")))
    print("Form thêm mới đã sẵn sàng.")
    delay_step()

    # --- BƯỚC 3: ĐIỀN THÔNG TIN VÀO FORM ---
    print("\n--- BẮT ĐẦU ĐIỀN THÔNG TIN VÀO FORM ---")
    
    # --- Xử lý các dropdown <ng-select> ---
    delay_step()
    handle_custom_dropdown(wait, "nguoiDeXuat_Ref", "Nguyễn")
    delay_step()
    handle_custom_dropdown(wait, "boPhanDeXuat_Ref", "ASD")
    delay_step()
    handle_custom_dropdown(wait, "nhanHang_Ref", "Milo")
    delay_step()
    handle_custom_dropdown(wait, "khachHang_Ref", "Milo cafe")
    delay_step()
    handle_custom_dropdown(wait, "benChiuPhiVanChuyen_Ref", "Khách hàng")
    delay_step()

    # --- Điền các trường văn bản, số và ngày tháng ---
    element = wait.until(EC.element_to_be_clickable((By.ID, "TongGiaTriDoiSauVAT")))
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.clear()
    element.send_keys("15000000")
    delay_step()
    
    date_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='ToTrinh_ThoiGianDoi']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", date_input)
    date_input.clear()
    date_input.send_keys("01/09/2025")
    date_input.send_keys(Keys.TAB)  #Dóng calender
    delay_step()

    date_input_den = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='ToTrinh_ThoiGianDoi_Den']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", date_input_den)
    date_input_den.clear()
    date_input_den.send_keys("15/09/2025")
    date_input_den.send_keys(Keys.TAB)  #Dóng calender
    delay_step()

    so_lan_nhan_hang = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='ToTrinh_SoLanNhanHang']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", so_lan_nhan_hang)
    so_lan_nhan_hang.clear()
    so_lan_nhan_hang.send_keys("3")
    delay_step()

    # loai_nhan = wait.until(EC.element_to_be_clickable((By.ID, "ToTrinh_LoaiNhan")))
    # driver.execute_script("arguments[0].scrollIntoView(true);", loai_nhan)
    # loai_nhan.clear()
    # loai_nhan.send_keys("Đồ uống")
    # delay_step()

    phu_trach_dau_ra = wait.until(EC.element_to_be_clickable((By.ID, "ToTrinh_NhanSuPhuTrach")))
    driver.execute_script("arguments[0].scrollIntoView(true);", phu_trach_dau_ra)
    phu_trach_dau_ra.send_keys("Vũ Thị Nga")
    delay_step()
    
    # --- Điền các trường textarea ---
    muc_dich_su_dung = wait.until(EC.element_to_be_clickable((By.ID, "ToTrinh_MucDichSuDung")))
    driver.execute_script("arguments[0].scrollIntoView(true);", muc_dich_su_dung)
    muc_dich_su_dung.send_keys("Chạy chiến dịch quảng cáo")
    delay_step()

    dich_vu_doi = wait.until(EC.element_to_be_clickable((By.ID, "ToTrinh_DichVuSanPhamDoiCuaVCCorp")))
    driver.execute_script("arguments[0].scrollIntoView(true);", dich_vu_doi)
    dich_vu_doi.send_keys("Banner Online")
    delay_step()

    # --- UPLOAD FILE ĐÍNH KÈM ---
    # Tìm và click nút "Chọn tệp"
    choose_file_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[normalize-space()='Chọn tệp']]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", choose_file_btn)
    choose_file_btn.click()
    delay_step(1)

    # Chờ trường input file xuất hiện và upload
    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][name='f_upload_normal']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
    file_path = r"C:\Users\ngavt\Downloads\BaoGiaHaiAnh.jpg"  # Sửa lại thành raw string
    file_input.send_keys(file_path)
    print(f"Đã chọn file '{file_path}' để upload.")
    delay_step()

    # --- NHẤN NÚT LƯU ---
    # Dùng XPath để tìm button có chứa span với text 'Lưu thông tin'
    save_btn_locator = (By.XPATH, "//button/span[normalize-space()='Lưu thông tin']")
    save_btn = wait.until(EC.element_to_be_clickable(save_btn_locator))
    save_btn.click()
    print("Đã nhấn nút 'Lưu thông tin'.")
    delay_step(5)

    print("\n--- HOÀN THÀNH ---")

except Exception as e:
    print(f"Lỗi ở bước này: {e}")
    traceback.print_exc()
finally:
    # Đảm bảo trình duyệt luôn được đóng dù có lỗi xảy ra
    driver.quit()
    print("Đã đóng trình duyệt.")