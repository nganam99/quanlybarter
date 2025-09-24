from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException 
import time
import traceback
from selenium import webdriver
# --- HÀM TRỢ GIÚP ĐỂ XỬ LÝ DROPDOWN PHỨC TẠP (NG-SELECT) ---
def handle_custom_dropdown(driver: webdriver ,wait: WebDriverWait, dropdown_name_attribute: str, option_text: str):
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