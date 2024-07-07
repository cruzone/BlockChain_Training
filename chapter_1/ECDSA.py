#conda install ecdsa

from ecdsa import SigningKey, SECP256k1, VerifyingKey
import hashlib

def sign_message(message, private_key):
    """
    使用ECDSA私钥对消息进行签名
    :param message: 要签名的消息（字符串）
    :param private_key: ECDSA私钥对象
    :return: 签名的字节串
    """
    # 将消息转换为字节串
    message_bytes = message.encode('utf-8')
    # 使用SHA-256哈希函数对消息进行哈希
    hashed_message = hashlib.sha256(message_bytes).digest()
    # 使用私钥对哈希后的消息进行签名
    signature = private_key.sign(hashed_message, hashfunc=hashlib.sha256)
    return signature

def verify_signature(message, signature, public_key):
    """
    使用ECDSA公钥验证签名
    :param message: 原始消息（字符串）
    :param signature: 签名的字节串
    :param public_key: ECDSA公钥对象
    :return: 布尔值，表示签名是否有效
    """
    # 将消息转换为字节串
    message_bytes = message.encode('utf-8')
    # 使用SHA-256哈希函数对消息进行哈希
    hashed_message = hashlib.sha256(message_bytes).digest()
    # 使用公钥和哈希后的消息验证签名
    return public_key.verify(signature, hashed_message, hashfunc=hashlib.sha256)

# 生成ECDSA密钥对
private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.get_verifying_key()

# 要签名的消息
message = "Hello, ECDSA!"

# 签名消息
signature = sign_message(message, private_key)

print("message:  ",message)
print("signature:  ",signature)
print("public_key:  ",public_key)


# 验证签名
is_valid = verify_signature(message, signature, public_key)
print(f"Signature is valid: {is_valid}")