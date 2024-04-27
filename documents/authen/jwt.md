# JSON WEB TOKEN

## 1. Cấu trúc JWT
JWT gồm 3 phần: 
    - **Header**:
        + Bao gồm 2 trường là: **typ**(loại token) và **alg**(thuật toán mã hóa có thể là HMAC, SHA256, RSA, HS256 hoặc RS256)
    - **Payload**:
        + Chứa các thông tin người dùng muốn gửi. Được mã hóa bằng Base64 và **có thể decode dễ dàng**.
    - **Signature**:
        + Phần chữ kí đưọc tạo ra bằng cách mã hóa **header**, **payload** bằng base64UrlEncoder. Sau đó chúng sẽ được ghép lại và ngăn cách nhau bằng 1 dấu ".". Tiếp theo nó được thêm một chuỗi **secret** khóa bí mật. Sau đó hash bằng thuật toán **H256**.

![JWT Structure](./imgs/1-jwt-structure.png)

```
Ví dụ:
// header
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

// payload
eyJhdWQiOlsidGVzdGp3dHJlc291cmNlaWQiXSwidXNlcl9uYW1lIjoiYWRtaW4iLCJzY29wZSI6WyJyZWFkIiwid3JpdGUiXSwiZXhwIjoxNTEzNzE

// Cộng chuỗi và thêm khóa bí mật rồi hash sẽ thành
9nRhBWiRoryc8fV5xRpTmw9iyJ6EM7WTGTjvCM1e36Q


=> Chuỗi cuối cùng:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsidGVzdGp3dHJlc291cmNlaWQiXSwidXNlcl9uYW1lIjoiYWRtaW4iLCJzY29wZSI6WyJyZWFkIiwid3JpdGUiXSwiZXhwIjoxNTEzNzE.9nRhBWiRoryc8fV5xRpTmw9iyJ6EM7WTGTjvCM1e36Q
```

## 2. Ưu nhược điểm.
**Ưu điểm:**

    - Đơn giản và dễ sử dụng: JWT có cấu trúc đơn giản, dễ dàng để hiểu và sử dụng.
    - Tiết kiệm tài nguyên: JWT được lưu trữ trên máy khách, giúp giảm tải cho máy chủ. Do đó, nó rất hữu ích trong các ứng dụng phân tán, nơi mà trạng thái có thể được lưu trữ tại nhiều vị trí khác nhau.
    - Độ tin cậy cao: JWT được mã hóa và ký, giúp ngăn chặn việc sửa đổi dữ liệu trên đường truyền.
    - Dữ liệu được lưu trữ trong token: JWT cho phép lưu trữ thông tin người dùng trong token, giúp giảm thiểu số lần truy vấn cơ sở dữ liệu.
    - Tích hợp dễ dàng: JWT có thể tích hợp với nhiều ngôn ngữ lập trình và framework.

**Nhược điểm:**

    - Không thể hủy bỏ token: Khi một token được tạo ra và gửi đến máy khách, không thể hủy bỏ nó trước khi hết thời gian sống hoặc thay đổi secret key và không thể chủ động force logout được. => có thể khắc phục bằng phương pháp mã hóa bất đối xứng.
    - Lưu trữ thông tin quá nhiều: Nếu lưu trữ quá nhiều thông tin người dùng trong token, kích thước của token có thể trở nên quá lớn. => khắc phục bằng cách giảm thiểu dữ liệu, chỉ lưu những thông tin cần thiết.
    - Rủi ro bảo mật: Nếu secret key của JWT bị lộ, thì hacker có thể giả mạo token và truy cập thông tin người dùng. => có thể khắc phục bằng phương pháp mã hóa bất đối xứng.
    - Không hỗ trợ quản lý phiên: JWT không hỗ trợ quản lý phiên như các giải pháp dựa trên cookie. Điều này có nghĩa là nếu bạn muốn hủy bỏ phiên của người dùng, bạn phải chờ cho JWT hết hạn hoặc thay đổi khóa bí mật. => có thể khắc phục bằng phương pháp mã hóa bất đối xứng.
    - Thời gian sống của token không linh hoạt: Nếu thời gian sống của token quá ngắn, người dùng sẽ phải đăng nhập quá thường xuyên. Nếu quá dài, thì việc bảo mật sẽ bị giảm sút. => áp dụng refresh token để khắc phục.

## 3. Cơ chế hoạt động JWT.
![cơ chế](./imgs/2-co-che.webp)

**B1**: Client gửi username, password tới server để login nhằm mục đích xác thực.
**B2**: Nếu login thành công server sẽ tạo ra token (jwt) và gửi về client.
**B3**: Client nhận token đó, rồi lưu trữ trên trình duyệt (cookies, localStorage, ..).
**B4**: Khi client gửi request tiếp theo tới server, request đó sẽ được đính kèm token nhằm mục đích xác thực.
**B5**: Server nhận được request và kiểm tra token. Nếu token hợp lệ thì gửi trả kết quả về client, còn không gửi thông báo chưa xác thực (403).

## 4. Tạo ra jwt trong python.
Cài đặt thư viện Pyjwt sử dụng pip:
```sh
pip install pyjwt
```
Sau khi thư viện được cài đặt, chúng ta có thể bắt đầu sử dụng JWTs để mã hóa và giải mã:

```python
import jwt  
      
header = {  
    "alg": "HS256",  
    "typ": "JWT"  
}  
      
payload = {  
    "sub": "1234967890",  
    "name": "John Doe",  
    "iat": 1516239022  
}  
      
secret = "Ravipass"  
      
encoded_jwt = jwt.encode(payload, secret, algorithm='HS256', headers=header)  
print(f"encoded_jwt = {encoded_jwt}") 
decoded_jwt=jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
print(f"decoded_jwt = {decoded_jwt}") 
)  
# Kết quả: 
# encoded_jwt = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0OTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.PcRV9bzaZH3sgyStgJreO7-QTaMPUcMq3EukYsNjWoo
# decoded_jwt = {'sub': '1234967890', 'name': 'John Doe', 'iat': 1516239022}
```

> Chú ý: HS256 là một thuật toán mã hóa bất đối xứng(mã hóa và giải mã cùng một khóa duy nhất, trong trường hợp này là secret)

