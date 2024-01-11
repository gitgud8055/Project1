# Bài tập project 1
## Maze game - Mô phỏng thuật toán tìm đường đi ngắn nhất

### 1. Bài toán:
Cho một ma trận n * n với vị trí bắt đầu, kết thúc và các ô bị chặn (không được đi vào). Tìm đường đi ngắn nhất từ điểm bắt đầu tới điểm kết thúc mà không đi qua các ô bị chặn.

### 2. Giải thích thuật toán:
Dựng một đồ thị vô hướng với các đỉnh là các ô của ma trận. Các cạnh của đồ thị nối giữa những cặp ô không bị chặn và có thể đi trực tiếp tới nhau. <br />
Code bao gồm 3 thuật toán và có thể chuyển đổi để xem sự khác biệt giữa các thuật toán với cùng đầu vào:
- Thuật toán Dijkstra
- Thuật toán A* (A star)
- Thuật toán Theta* (Theta star)
#### 2.1 Thuật toán Dijkstra:
Sử dụng BFS để tìm đường đi ngắn nhất. <br />
Độ phức tạp: O(n + m) ~ O(5 * n) với n là số đỉnh và m là số cạnh của đồ thị
#### 2.2 Thuật toán A*:
Gọi node là một ô trống bất kì. Ta xét hàm đánh giá:
```
T(node) = F(node) + G(node)
với F(node) là độ dài đường đi ngắn nhất tính từ điểm bắt đầu tới node
    G(node) là giá trị hàm heuristic của node, được tính bằng khoảng cách Halminton từ node tới điểm kết thúc
```
Thực hiện thuật toán A* với hàm đánh giá trên, ta thu được kết quả <br/>
Độ phức tạp: O((n + m) * log(n)) 
#### 2.3 Thuật toán Theta*:
Ta cũng xét hàm đánh giá T(node) tương tự với thuật toán A*. Nhưng ở thuật toán này, ta sẽ cho phép đi theo đường chéo của ma trận. <br/>
Độ phức tạp: O((n + m) * log(n))

### 3. Nhận xét:
- Thuật toán Dijkstra: Tuy đây là thuật toán có độ phức tạp nhỏ nhất, nhưng đây cũng là thuật toán có thời gian tìm kiếm lâu nhất do phải xét hết các hướng có thể xảy ra
- Thuật toán A*: đây là một phiên bản cải tiến của thuật toán Dijkstra, từ thực nghiệm cho thấy thuật toán này cho ra kết quả khá nhanh. Tuy đây có thể không phải đường đi ngắn nhất mà ta cần tìm, nhưng nó cũng là một đường đi "gần" ngắn nhất. Đổi lại, ta có thể tìm ra đường đi đó một cách nhanh chóng.
- Thuật toán Theta*: đây là một phiên bản khác của thuật toán A*, nhằm đánh giá tốc độ thực thi trong các điều kiện khác nhau. Dựa theo độ phức tạp thuật toán, đây là thuật toán có độ phức tạp lớn nhất, nhưng lại có thể tìm ra kết quả thỏa mãn trong thời gian ngắn nhất.
### 4. Hướng dẫn sử dụng và lưu ý:
Những thư viện cần thiết để thực thi chương trình: pygame <br/>
Giao diện bao gồm: bảng ma trận, các lựa chọn thuật toán và thông báo thuật toán đang được sử dụng. <br/>
Ý nghĩa của các màu trong ma trận:
- Màu xanh lam (blue): Điểm bắt đầu
- Màu xanh lục (green): Điểm kết thúc
- Màu vàng (yellow): Những ô đã đi qua
- Màu đỏ (red): Những ô sắp đến (đang nằm trong hàng đợi)
- Màu đen (black): Những ô bị chặn
- Màu tím (purple): Đường đi từ điểm bắt đầu tới ô hiện tại (truy vết)

Để tạo ra ma trận, ta sử dụng chuột phải click vào một ô bất kì. Đó sẽ là:
- Ô bắt đầu nếu chưa tồn tại ô bắt đầu
- Ô kết thúc nếu đã có ô bắt đầu và chưa tồn tại ô kết thúc
- Ô bị chặn nếu không thỏa mãn 2 trường hợp trên

Một số tính năng:
- Sử dụng chuột phải để xóa đi một ô nếu vẽ nhầm
- Chuyển đổi thuật toán mà vẫn giữ nguyên đầu vào bằng cách click chuột vào tên các thuật toán ở phía bên phải
- Ấn **Enter** để bắt đầu thực hiện thuật toán đã chọn
- Khi thuật toán đang được thực thi, ấn **Space** để tạm dừng thuật toán, cho phép ta xem trạng thái hiện tại của đồ thị. Trong lúc đó, nếu click chuột vào một ô đã đi qua, sẽ có một đường màu tím (purple) để trace back lại đường đi ngắn nhất tới nó
- Khi thực hiện thuật toán, mỗi ô đã đi qua sẽ có một giá trị là độ dài đường đi ngắn nhất từ điểm bắt đầu tới điểm đó.
- Khi thuật toán kết thúc sẽ tự động có một đường màu tím (purple) để trace back lại đường đi ngắn nhất từ điểm bắt đầu tới điểm kết thúc
- Ấn nút **C** để vẽ lại ma trận mới.
