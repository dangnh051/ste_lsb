import cv2
import numpy as np
from sympy import nextprime

def blum_blum_shub(seed, length, p=383, q=503):
    """Tạo chuỗi số ngẫu nhiên bằng thuật toán Blum Blum Shub"""
    n = p * q
    x = (seed * seed) % n
    bit_sequence = []
    for _ in range(length):
        x = (x * x) % n
        bit_sequence.append(x % 2)
    return bit_sequence

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def hide_data(image_path, message, seed):
    # Đọc ảnh
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    max_capacity = h * w * 3 // 8  # Tính dung lượng tối đa có thể giấu

    message_bits = text_to_bits(message)
    if len(message_bits) > max_capacity:
        raise ValueError("Thông điệp quá dài so với ảnh.")

    # Sinh vị trí nhúng bằng thuật toán BBS
    positions = blum_blum_shub(seed, len(message_bits), nextprime(h), nextprime(w))
    indices = sorted(range(len(message_bits)), key=lambda i: positions[i])

    flat_img = img.flatten()
    modified_pixels = []  # Danh sách lưu vị trí pixel bị thay đổi
    
    # Nhúng tin vào ảnh tại vị trí ngẫu nhiên
    for i, bit in zip(indices, message_bits):
        old_value = flat_img[i]
        new_value = (old_value & ~1) | int(bit)  # Thay đổi bit LSB
        flat_img[i] = new_value
        
        if old_value != new_value:  # Kiểm tra nếu pixel bị thay đổi
            pixel_index = i // 3  # Mỗi pixel có 3 giá trị (R, G, B)
            x, y = pixel_index % w, pixel_index // w
            modified_pixels.append((x, y))

    # Lưu ảnh đã nhúng
    img_stego = flat_img.reshape(img.shape)
    cv2.imwrite("stego_image.png", img_stego)
    
    # In ra tọa độ 20 pixel đầu tiên bị chỉnh sửa
    print("✅ Đã giấu tin thành công! 🔑 Nhớ Seed:", seed)
    print("📍 20 pixel đầu tiên bị thay đổi:")
    for coord in modified_pixels[:20]:
        print(coord)

# Chạy chương trình
if __name__ == "__main__":
    image_path = input("📷 Nhập đường dẫn ảnh: ")
    message = input("✉️ Nhập thông điệp cần giấu: ")
    seed = int(input("🔑 Nhập Seed (số nguyên): "))
    hide_data(image_path, message, seed)
