from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_key_pair():
    # RSA 키 쌍 생성 (2048 비트)
    key = RSA.generate(2048)

    # 공개 키와 개인 키 반환
    public_key = key.publickey().export_key().decode('utf-8')
    private_key = key.export_key().decode('utf-8')

    return public_key, private_key

def encrypt_text(text, public_key):
    # 텍스트를 바이트 문자열로 변환
    text_bytes = text.encode('utf-8')

    # 공개 키 로드
    public_key = RSA.import_key(public_key)

    # RSA 암호화 객체 생성
    cipher_rsa = PKCS1_OAEP.new(public_key)

    # 텍스트 암호화
    encrypted_text = cipher_rsa.encrypt(text_bytes)

    # 암호화된 텍스트를 Base64로 인코딩하여 반환
    return encrypted_text.hex()

def decrypt_text(encrypted_text, private_key):
    # 암호화된 텍스트를 바이트 문자열로 변환
    encrypted_text_bytes = bytes.fromhex(encrypted_text)

    # 개인 키 로드
    private_key = RSA.import_key(private_key)

    # RSA 복호화 객체 생성
    cipher_rsa = PKCS1_OAEP.new(private_key)

    # 텍스트 복호화
    decrypted_text = cipher_rsa.decrypt(encrypted_text_bytes)

    # 복호화된 텍스트를 문자열로 디코딩하여 반환
    return decrypted_text.decode('utf-8')

# 암호화할 경로
text = 'Original/1/jiwoo/test3.png'

# RSA 키 쌍 생성
public_key, private_key = generate_key_pair()

# 텍스트 암호화
encrypted_text = encrypt_text(text, public_key)
print('암호화된 텍스트:', encrypted_text)

# 텍스트 복호화
decrypted_text = decrypt_text(encrypted_text, private_key)
print('복호화된 텍스트:', decrypted_text)

# 생성된 공개 키와 개인 키 출력
print('공개 키:\n', public_key)
print('개인 키:\n', private_key)
