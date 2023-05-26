from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import binascii

def encrypt_path(path, public_key_path):
    # 대칭키 생성
    key = get_random_bytes(16)

    # 경로를 바이트 문자열로 변환 및 패딩
    path_bytes = pad(path.encode('utf-8'), 16)

    # 공개 키 로드
    with open(public_key_path, 'rb') as file:
        public_key = RSA.import_key(file.read())

    # 대칭키 암호화
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(key)

    # AES-CBC 암호화
    cipher_aes = AES.new(key, AES.MODE_CBC)
    encrypted_path = cipher_aes.encrypt(path_bytes)

    # 암호화된 대칭키와 경로를 Base64로 인코딩하여 반환
    return binascii.hexlify(encrypted_key).decode('utf-8'), binascii.hexlify(cipher_aes.iv).decode('utf-8'), binascii.hexlify(encrypted_path).decode('utf-8')

# 테스트용 공개 키 파일 경로
public_key_path = 'public_key.pem'

# 암호화할 경로
original_path = 'Original/1/jiwoo/test3.png'

# 경로 암호화
encrypted_key, iv, encrypted_path = encrypt_path(original_path, public_key_path)

# 디코딩하여 바이트로 변환
encrypted_key = bytes.fromhex(encrypted_key)
iv = bytes.fromhex(iv)
encrypted_path = bytes.fromhex(encrypted_path)

print('암호화된 대칭키:', encrypted_key)
print('IV:', iv)
print('암호화된 경로:', encrypted_path)
