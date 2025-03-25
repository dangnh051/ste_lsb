import cv2
import numpy as np

def text_to_bits(text):
    """Chuyển đổi văn bản thành chuỗi bit nhị phân"""
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits):
    """Chuyển đổi chuỗi bit nhị phân về văn bản"""
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def hide_data(image_path, message):
    # Đọc ảnh
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    max_capacity = h * w * 3 // 8  # Tính toán dung lượng tối đa có thể giấu

    # Chuyển đổi thông điệp thành bit
    message_bits = text_to_bits(message)
    if len(message_bits) > max_capacity:
        raise ValueError("Thông điệp quá dài so với ảnh.")

    # Nhúng tin theo thứ tự từ pixel đầu tiên
    flat_img = img.flatten()
    modified_pixels = []  # Danh sách lưu các tọa độ bị thay đổi

    for i, bit in enumerate(message_bits):
        if flat_img[i] % 2 != int(bit):  # Kiểm tra nếu cần thay đổi
            flat_img[i] = (flat_img[i] & ~1) | int(bit)
            pixel_index = i // 3  # Mỗi pixel có 3 kênh màu
            x, y = pixel_index % w, pixel_index // w  # Tính tọa độ (x, y)
            modified_pixels.append((x, y))  # Lưu lại tọa độ

    # Lưu ảnh đã nhúng tin
    img_stego = flat_img.reshape(img.shape)
    cv2.imwrite("stego_image.png", img_stego)

    # In tọa độ các pixel đã thay đổi
    print("✅ Đã giấu tin thành công! Các pixel bị thay đổi:")
    for coord in modified_pixels[:20]:  # In ra 20 tọa độ đầu tiên để dễ kiểm tra
        print(coord)
    print("...(và nhiều pixel khác)")

# Chạy chương trình
if __name__ == "__main__":
    image_path = input("📷 Nhập đường dẫn ảnh: ")
    message = input("✉️ Nhập thông điệp cần giấu: ")
    hide_data(image_path, message)
