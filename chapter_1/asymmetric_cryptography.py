# conda install cryptography

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import signing
from cryptography.exceptions import InvalidSignature


# 生成EC密钥对
def generate_ec_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    # 将公钥和私钥保存为PEM格式，便于存储和传输
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem


# 创建数字签名
def sign_data(private_key_pem, data):
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=None
    )
    signer = private_key.signer(
        signature_algorithm=ec.ECDSA(hashes.SHA256())
    )
    signer.update(data.encode())
    signature = signer.finalize()
    return signature


# 验证数字签名
def verify_signature(public_key_pem, data, signature):
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=None
    )
    verifier = public_key.verifier(
        signature,
        ec.ECDSA(hashes.SHA256())
    )
    verifier.update(data.encode())
    try:
        verifier.verify()
        print("Signature is valid.")
    except InvalidSignature:
        print("Signature is invalid.")

    # 示例用法


if __name__ == "__main__":
    private_key_pem, public_key_pem = generate_ec_keypair()

    # 假设我们要签名的数据
    data = "Hello, Blockchain!"

    # 创建签名
    signature = sign_data(private_key_pem, data)

    # 验证签名
    verify_signature(public_key_pem, data, signature)