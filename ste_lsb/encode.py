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

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def hide_data(image_path, message, seed):
    # Đọc ảnh
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    max_capacity = h * w * 3 // 8

    message_bits = text_to_bits(message)
    if len(message_bits) > max_capacity:
        raise ValueError("Thông điệp quá dài so với ảnh.")

    # Tạo chuỗi vị trí ngẫu nhiên bằng BBS
    positions = blum_blum_shub(seed, len(message_bits), nextprime(h), nextprime(w))
    indices = sorted(range(len(message_bits)), key=lambda i: positions[i])

    # Nhúng tin vào ảnh
    flat_img = img.flatten()
    for i, bit in zip(indices, message_bits):
        flat_img[i] = (flat_img[i] & ~1) | int(bit)

    # Lưu ảnh đã nhúng
    img_stego = flat_img.reshape(img.shape)
    cv2.imwrite("stego_image.png", img_stego)
    print(f"✅ Đã giấu tin thành công! 🔑 Nhớ Seed: {seed}")

# Chạy chương trình
if __name__ == "__main__":
    image_path = input("📷 Nhập đường dẫn ảnh: ")
    message = input("✉️ Nhập thông điệp cần giấu: ")
    seed = int(input("🔑 Nhập Seed (số nguyên): "))
    hide_data(image_path, message, seed)
