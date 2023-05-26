from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def encrypt_path(path, public_key_path):
    # 경로를 바이트 문자열로 변환
    path_bytes = path.encode('utf-8')

    # 공개 키 로드
    with open(public_key_path, 'r') as file:
        public_key = RSA.import_key(file.read())

    # RSA 암호화 객체 생성
    cipher_rsa = PKCS1_OAEP.new(public_key)

    # 경로 암호화
    encrypted_path = cipher_rsa.encrypt(path_bytes)

    # 암호화된 경로를 Base64로 인코딩하여 반환
    return encrypted_path.hex()

def decrypt_path(encrypted_path, private_key_path):
    # 암호화된 경로를 바이트 문자열로 변환
    encrypted_path_bytes = bytes.fromhex(encrypted_path)

    # 개인 키 로드
    with open(private_key_path, 'r') as file:
        private_key = RSA.import_key(file.read())

    # RSA 복호화 객체 생성
    cipher_rsa = PKCS1_OAEP.new(private_key)

    # 경로 복호화
    decrypted_path = cipher_rsa.decrypt(encrypted_path_bytes)

    # 복호화된 경로를 문자열로 디코딩하여 반환
    return decrypted_path.decode('utf-8')

# 테스트용 공개 키와 개인 키 파일 경로
public_key_path = 'public_key.pem'
private_key_path = 'private_key.pem'

# 암호화할 경로
original_path = '/RSA/test.txt'

# 경로 암호화
encrypted_path = encrypt_path(original_path, public_key_path)
print('암호화된 경로:', encrypted_path)

# 암호화된 경로 복호화
decrypted_path = decrypt_path(encrypted_path, private_key_path)
print('복호화된 경로:', decrypted_path)
