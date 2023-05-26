from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import binascii

def decrypt_path(encrypted_key, iv, encrypted_path, private_key_path):
    # 암호화된 대칭키, IV, 경로를 바이트 문자열로 변환
    try:
        encrypted_key_bytes = bytes.fromhex(encrypted_key)
        iv_bytes = bytes.fromhex(iv)
        encrypted_path_bytes = bytes.fromhex(encrypted_path)
    except ValueError:
        raise ValueError("Invalid hexadecimal format")

    # 개인 키 로드
    with open(private_key_path, 'r') as file:
        private_key = RSA.import_key(file.read())

    # RSA 복호화
    cipher_rsa = PKCS1_OAEP.new(private_key)
    key = cipher_rsa.decrypt(encrypted_key_bytes)

    # AES-CBC 복호화
    cipher_aes = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted_path = cipher_aes.decrypt(encrypted_path_bytes)

    # 복호화된 경로를 문자열로 디코딩하여 반환
    return decrypted_path.decode('utf-8')

# 테스트용 개인 키 파일 경로
private_key_path = 'private_key.pem'

# 복호화할 암호화된 대칭키, IV, 경로
encrypted_key = '7c54c25c3529045b73d0e353fa02fed42540901da825788bd363dc9c717872fc4a5c91823cc6603a6b90e843d6c5b35b4d46fb89bd0daadede68a87df82a92e3a9e04bdf0064cdf9f17d4daeeecd299e60c37a38b2d77302d5a888eb0a29c3d228734845b06ba58685ae390053390f66f764e7e6d083805b58f6afa0f0039f5a16d80d4bd986fbbad5a06b2d85ff376917db1a7475d2c9ef911451b64391d86b0b8be0d01325d171354e9d70fa7153971754cbdfec358d79ee51d86917bf9439585bd9a5185b92aa6441c4ae6b7d9492def532be9d7e7c2bc430f3e412294b28ce74f23fd6c73df8d6c04bbd01cdd6c9c92a0182f43a9fbed3a2fec5b'
iv = 'c87e94bc98403c2c6a7ed7d62871a38c'
encrypted_path = '01c056563787d646eb4725b0329d7e8b35900b29c37419ef5cba1e568aef9a3f'

# 경로 복호화
try:
    decrypted_path = decrypt_path(encrypted_key, iv, encrypted_path, private_key_path)
    print('복호화된 경로:', decrypted_path)
except ValueError as e:
    print('에러:', str(e))
