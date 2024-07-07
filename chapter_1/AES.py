# conda install pycryptodome


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor


def aes_encrypt(plaintext, key):
    # AES要求密钥长度必须是16（AES-128）、24（AES-192）或32（AES-256）字节
    # 这里我们使用AES-256
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes for AES-256")

        # AES块大小是16字节
    cipher = AES.new(key, AES.MODE_CBC)
    var = AES.new

    ct_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    iv = cipher.iv  # 初始化向量
    return iv + ct_bytes


def aes_decrypt(ciphertext, key):
    # 分离初始化向量和密文
    iv = ciphertext[:AES.block_size]
    ct = ciphertext[AES.block_size:]

    # 使用相同的密钥和IV进行解密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')


# 示例密钥（必须是32字节）
key = get_random_bytes(32)

# 要加密的明文
plaintext = "Hello, AES Encryption!"

# 加密
ciphertext = aes_encrypt(plaintext, key)
print("Ciphertext:", ciphertext.hex())

# 解密
decrypted_text = aes_decrypt(ciphertext, key)
print("Decrypted Text:", decrypted_text)


 