export http_proxy=http://proxy.cyberspace.vn:3128
export https_proxy=http://proxy.cyberspace.vn:3128

https://viblo.asia/p/huong-dan-co-ban-framework-fastapi-tu-a-z-phan-1-V3m5W0oyKO7


docker run -d --name zookeeper-server -e ALLOW_ANONYMOUS_LOGIN=yes --network kafka-network hub.vtcc.vn:8989/bitnami/zookeeper

docker run -d --name kafka-server --hostname kafka-server \
    --network kafka-network \
    -e KAFKA_CFG_NODE_ID=0 \
    -e KAFKA_CFG_PROCESS_ROLES=controller,broker \
    -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
    -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
    -e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-server:9093 \
    -e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    hub.vtcc.vn:8989/bitnami/kafka

TARGET => từ bài 1 đến bài 56

# Các task chưa có time để làm
1. Check xem hệ thống quá tải hay không?
    1.1. Check xem có bn connection đang đến.
    1.2. Check xem hệ thống quá tải không bằng cách check process.
2. Viết lại phần response của hệ thống.
3. Viết lại phần handle Exception sư dung Middleware.
4. Chưa hadle login với nhiều device
    - Biến đổi refresh_token thành list và lưu các refresh_token ở từng thiết bị trong list đó.
5. Sử dụng fastapi_session để quản lý phiên.
6. Tạo hệ thống phát hiện hacker đã chiếm quyền 
    - Thông thường thì một access token sẽ có 1 khoảng thời gian sống là khá ngắn.
    - Giả sử 1 hacker tấn công và có được cả refresh token và access token. Khi đó cả user và hacker để có thể truy cập được hệ thống. 
    Ta cũng giả sử rằng hệ thống khá là trặt trẽ trong việc lấy lại mật khẩu để tránh trường hợp hacker dùng tính năng lấy lại mật khẩu để đặt lại mật khẩu mới. 
    - Khi thời điểm access token hết hạn thì user và hacker ai đang trong phiên trước thì sẽ được cấp 1 access_token mới và refresh_token mới và refresh token cũ sẽ được lưu vào refresh_token_used. Ở một thời điểm nào đó người còn lại đăng nhập thì hệ thống sẽ check xem refresh_token đó có trong list refresh_token_used không? Nếu có tức là 1 là server bị hack và 2 là người dùng đã để mất token. Khi đó ta sẽ tước hết quyền đăng nhập của 2 cá thể đó bằng cách xóa luôn bản ghi chứa các token đó và gửi 1 mail(nếu có) để yêu cầu người dùng đặt lại mật khẩu. Hoặc là bắt nguoif dùng đăng nhập lại để hệ thống cấp lại 2 token. 

7. Sử dụng session trong fastapi
8. Kết hợp Factory và Strategy trong Product
9. findAll cần phân trang
10. update thì cần tạo 1 hàm update, select có 1 trường truyền vào collums là 1 tuple các cột cần lấy, 1 trường biểu thị là mình sẽ lấy các column kia hay không(Ví dụ nếu nó là dương thì sẽ lấy còn là âm thì sẽ không lấy). Hàm select này có thể áp dụng theo trường ABC jj đó
11. Update xem xét kiểm tra các giá trị null có đưọc chấp nhận không?
12. Sử dụng redis để lưu cache và các hàm đưọc sử dụng cho các kiểu dữ liệu redis như str(bao gồm cả text và number), set, list, hash( giống dict của python ), zset.
13. Sử dụng redis transaction