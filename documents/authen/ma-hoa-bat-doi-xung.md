# Xác thực JWT cũng mã hóa bất đối xứng

Reference:
    - [Generating Encrypted Key Pairs In Python](https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b)

Thay vì sử dụng chung 1 mã để mã hóa và giải mã như mã hóa đối xứng thì ở đây chúng ta sẽ có 2 KEY: **public key** và **private key**
- **Private key**: đưọc sử dụng để mã hóa thông tin tạo ra JWT. Token này đưọc đưa cho user lưu trữ và sẽ không đưọc lưu vào bất kì đâu trong server(kể cả database).

- **Public key**: Đưọc dùng để giải mã JWT đó và đưọc lưu vào DB của server. 

Khi một hacker muốn tấn công hệ thống này thì phải có đưọc cả 2 key. Làm tăng độ khó cho bài toán.

## Cách thức triển khai.
![Cach thuc trien khai](./imgs/3-xac-thuc-jwt-cung-ma-hoa-bat-doi-xung.webp)

Để triển khai ta cần cài đặt thư viện: 
```sh
pip install cryptography Pyjwt
```

Chương trình:
```python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import jwt

# Generate RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)

public_key = private_key.public_key()

# Example data
payload = {'user_id': 123456}

# Encode JWT token
jwt_token = jwt.encode(payload, private_key, algorithm='RS256')

print("Encoded JWT token:", jwt_token)

# Decode JWT token
decoded_payload = jwt.decode(jwt_token, public_key, algorithms=['RS256'])

print("Decoded payload:", decoded_payload)

# Kết quả:
# Encoded JWT token: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NTZ9.nzbs2CMhYfrs0mDgzZjtuIusRT7sC7340l4DrmxwXWxRF87QnE4nPWM7DG9E0LvFD171q0F88KVjJRXSf1OfygSP33Tac3C7b9gdz9U2Qm-5fkZj7jvGQ-8RaVCxbTcblh4yn4et8SuXfS5m7DmOWYlq8Qw1w-Xz9cRf5WA-Vt2hhjWYFhwmQTx7P-bWa4ztouacYCnPsHEQkPpNqKfsZFzWqFfVnZbBNiRBzkDafvq-q1FZavPOKcBhjuBlaoa-Q0RIym___O7pc9tCEXwGNGOVRmUX7fAQ-hIlIT0jZzgKfWH7OGIUwAyXc-MafnXpBNLIjM15l0lcAbEKaAN4aQ

# Decoded payload: {'user_id': 123456}

```
**Giải thích**: 
- **default_backend** sẽ giúp hệ thống tự chọn backend phù hợp với hệ thống như là OpenSSL, CommonCrypto trên MacOS hay Windows CNG trong windows.

## PEM
Là một định dạng dạng string của private key. Là một dạng thể hiện của private key được gửi cho người dùng.

Để tạo một key PEM.

```python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import jwt

# Generate RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

public_key = private_key.public_key()

# Serialize keys to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
```

Nêú muốn mã hóa key-pem một lần nữa để tăng tính bảo mật thì ta sử dụng **serialization.BestAvailableEncryption()** với tham số truyền vào là một secret_key khác:

```python
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

public_key = private_key.public_key()

# Serialize keys to PEM format with encryption
password = b'mypassword'  # Mật khẩu cho mã hóa khóa riêng tư
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(password)
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

```
### Quá trình thực hiện khi một người dùng upload key PEM
TO-DO: 