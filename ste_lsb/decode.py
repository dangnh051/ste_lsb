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

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def extract_data(stego_image_path, message_length, seed):
    # Đọc ảnh
    img = cv2.imread(stego_image_path)
    h, w, _ = img.shape

    # Tạo chuỗi vị trí ngẫu nhiên bằng BBS
    positions = blum_blum_shub(seed, message_length, nextprime(h), nextprime(w))
    indices = sorted(range(message_length), key=lambda i: positions[i])

    # Trích xuất bit từ ảnh
    flat_img = img.flatten()
    extracted_bits = ''.join(str(flat_img[i] & 1) for i in indices)

    # Chuyển bit thành văn bản
    message = bits_to_text(extracted_bits)
    print(f"🔓 Thông điệp đã giải mã: {message}")
    return message

# Chạy chương trình
if __name__ == "__main__":
    stego_image_path = input("📷 Nhập đường dẫn ảnh chứa thông điệp: ")
    message_length = int(input("📏 Nhập độ dài thông điệp đã giấu (tính theo bit): "))
    seed = int(input("🔑 Nhập Seed để giải mã: "))
    extract_data(stego_image_path, message_length, seed)
