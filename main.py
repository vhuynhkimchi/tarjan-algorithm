import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# --- CÁC BIẾN TOÀN CỤC ---
root = None # Cửa sổ chính
txt_input = None # Nhập liệu đồ thị
lbl_stats = None # Thống kê đồ thị
entry_vertices = None # Nhập số đỉnh lẻ (không có cạnh)
ax = None # Trục vẽ matplotlib 
canvas = None # Canvas matplotlib
txt_log = None      # Hiển thị các bước DFS
tree_table = None   # Bảng Disc/Low/Parent
txt_bridges_list = None # Danh sách cầu tìm được
txt_verify = None       # Kiểm chứng cầu với BFS

# Biến để kiểm soát Animation
ANIMATION_SPEED = 0.8 # Giây

# --- HÀM VẼ LẠI TRONG QUÁ TRÌNH CHẠY (ANIMATION) ---
def update_canvas_step(G, pos, node_colors, edge_colors, labels_map, title):
    """Hàm phụ trợ để vẽ lại đồ thị trong vòng lặp DFS"""
    ax.clear()
    
    # Vẽ cạnh
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=2)
    
    # Vẽ đỉnh
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=1000)
    
    # Vẽ nhãn
    nx.draw_networkx_labels(G, pos, labels=labels_map, ax=ax, font_size=8, font_weight='bold')
    
    ax.set_title(title, fontsize=10)
    canvas.draw()
    root.update() # Quan trọng: Cập nhật giao diện ngay lập tức
    time.sleep(ANIMATION_SPEED)

# --- THUẬT TOÁN TARJAN + VISUALIZATION ---
def run_tarjan_visual(G, pos):
    disc = {} # Thời gian phát hiện
    low = {} # Giá trị low
    time_counter = 0 # Bộ đếm thời gian toàn cục
    bridges = [] # Danh sách cầu tìm được
    parent = {node: None for node in G.nodes()} # Cha của mỗi đỉnh
    visited = set() # Tập đỉnh đã thăm
    logs = [] # Log các bước thực hiện
    final_data = [] # Dữ liệu bảng

    # Màu sắc mặc định
    node_colors = ['skyblue'] * len(G.nodes()) 
    edge_colors = ['black'] * len(G.edges())
    node_list = list(G.nodes())
    edge_list = list(G.edges())

    # Hàm lấy index để đổi màu
    def get_node_idx(n): return node_list.index(n)
    
    # Map nhãn hiển thị hiện tại
    def get_labels():
        l_map = {}
        for n in G.nodes():
            d = disc.get(n, "?")
            l = low.get(n, "?")
            l_map[n] = f"{n}\n({d}/{l})"
        return l_map

    def dfs(u):
        nonlocal time_counter 
        visited.add(u)
        disc[u] = low[u] = time_counter
        time_counter += 1
        
        # --- VISUAL: Đang thăm U (Màu vàng) ---
        node_colors[get_node_idx(u)] = 'yellow' 
        logs.append(f"-> Thăm {u}: disc={disc[u]}, low={low[u]}")
        update_canvas_step(G, pos, node_colors, edge_colors, get_labels(), f"Đang thăm đỉnh {u}")

        for v in G.neighbors(u):
            if v == parent[u]:
                continue
            
            if v in visited:
                # Cập nhật low khi gặp cạnh ngược
                old_low = low[u]
                low[u] = min(low[u], disc[v])
                logs.append(f"   ! Cạnh ngược ({u}-{v}): low[{u}] update {old_low}->{low[u]}")
                update_canvas_step(G, pos, node_colors, edge_colors, get_labels(), f"Phát hiện cạnh ngược {u}-{v}")
            else:
                parent[v] = u
                logs.append(f"   + Đi xuống ({u}->{v})")
                dfs(v)
                
                # Quay lui
                old_low = low[u]
                low[u] = min(low[u], low[v])
                logs.append(f"   < Quay lui {v}->{u}: low[{u}] update {old_low}->{low[u]}")
                update_canvas_step(G, pos, node_colors, edge_colors, get_labels(), f"Quay lui về {u}")

                if low[v] > disc[u]:
                    bridges.append((u, v))
                    logs.append(f"   *** CẦU: {u}-{v}")
                    # --- VISUAL: Tìm thấy cầu (Tô đỏ cạnh này) ---
                    # Tìm index cạnh để tô đỏ
                    try:
                        e_idx = edge_list.index((u, v))
                    except:
                        e_idx = edge_list.index((v, u))
                    edge_colors[e_idx] = 'red'
                    update_canvas_step(G, pos, node_colors, edge_colors, get_labels(), f"PHÁT HIỆN CẦU {u}-{v}")

        # --- VISUAL: Đã duyệt xong U (Màu xanh lá) ---
        node_colors[get_node_idx(u)] = '#90EE90' 
        update_canvas_step(G, pos, node_colors, edge_colors, get_labels(), f"Hoàn tất đỉnh {u}")

    # Chạy DFS
    for node in G.nodes():
        if node not in visited:
            dfs(node)

    # Chuẩn bị dữ liệu trả về
    for node in G.nodes():
        final_data.append((node, disc[node], low[node], parent[node]))
    
    return bridges, logs, final_data

# --- HÀM KIỂM CHỨNG BẰNG BFS (BRUTE FORCE) ---
def verify_bridges_with_bfs(G, bridges):
    """
    Kiểm tra lại tính chất cầu: Xóa cạnh -> Số TPLT tăng lên -> Là cầu
    """
    report = []
    initial_components = nx.number_connected_components(G)
    report.append(f"Số TPLT ban đầu: {initial_components}\n")
    
    if not bridges:
        report.append("-> Danh sách cầu rỗng. Không cần kiểm chứng.")
        return report

    for u, v in bridges:
        # Tạo bản sao graph để xóa thử
        G_temp = G.copy()
        if G_temp.has_edge(u, v):
            G_temp.remove_edge(u, v)
            
            # Kiểm tra số thành phần liên thông sau khi xóa (Dùng BFS ngầm định trong nx)
            new_components = nx.number_connected_components(G_temp)
            
            status = "ĐÚNG" if new_components > initial_components else "SAI"
            report.append(f"- Cạnh ({u}, {v}): Xóa xong có {new_components} TPLT. \n  => Kết luận: {status} là Cầu.")
        else:
            report.append(f"- Cạnh ({u}, {v}): Lỗi không tìm thấy cạnh.")
            
    return report

# --- HÀM XỬ LÝ CHÍNH ---
def start_processing():
    input_data = txt_input.get("1.0", tk.END).strip()
    if not input_data:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập dữ liệu!")
        return

    # 1. Dựng đồ thị
    G = nx.Graph()
    try:
        lines = input_data.split('\n')
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2: G.add_edge(parts[0], parts[1])
            elif len(parts) == 1: G.add_node(parts[0])
        
        # Thêm đỉnh lẻ
        num_v = entry_vertices.get().strip()
        if num_v.isdigit():
            for i in range(1, int(num_v)+1):
                if str(i) not in G.nodes(): G.add_node(str(i))
    except Exception as e:
        messagebox.showerror("Lỗi nhập liệu", str(e))
        return

    # 2. Chuẩn bị Visual
    pos = nx.spring_layout(G, seed=42) # Cố định vị trí
    
    # Reset các khung hiển thị
    txt_log.config(state=tk.NORMAL); txt_log.delete("1.0", tk.END)
    txt_bridges_list.config(state=tk.NORMAL); txt_bridges_list.delete("1.0", tk.END)
    txt_verify.config(state=tk.NORMAL); txt_verify.delete("1.0", tk.END)
    for row in tree_table.get_children(): tree_table.delete(row)

    # --- ĐO THỜI GIAN THUẬT TOÁN (ALGORITHM TIME) ---
    # Chạy thử thuật toán tìm cầu thuần túy (không visual) để đo tốc độ tính toán
    t_start_algo = time.perf_counter()
    list(nx.bridges(G)) # Dùng hàm thư viện hoặc DFS thuần để đo tải CPU
    t_end_algo = time.perf_counter()
    algo_time_ms = (t_end_algo - t_start_algo) * 1000 # Đổi ra ms

    # --- ĐO THỜI GIAN MÔ PHỎNG (ANIMATION TIME) ---
    t_start_anim = time.perf_counter()
    
    # 3. CHẠY TARJAN + VISUALIZATION
    bridges, logs, table_data = run_tarjan_visual(G, pos)
    
    t_end_anim = time.perf_counter()
    anim_time_s = t_end_anim - t_start_anim # Tính bằng giây

    # 4. HIỂN THỊ KẾT QUẢ TARJAN
    # Log
    for l in logs: txt_log.insert(tk.END, l + "\n")
    txt_log.config(state=tk.DISABLED)
    
    # Bảng
    for r in table_data: tree_table.insert("", tk.END, values=r)
    
    # List Cầu
    if bridges:
        for b in bridges: txt_bridges_list.insert(tk.END, f"{b[0]} - {b[1]}\n")
    else:
        txt_bridges_list.insert(tk.END, "Không có cầu nào.")
    txt_bridges_list.config(state=tk.DISABLED)

    # --- CẬP NHẬT NHÃN THỐNG KÊ KÈM THỜI GIAN ---
    lbl_stats.config(text=f"Đỉnh: {G.number_of_nodes()} | Cạnh: {G.number_of_edges()} | Cầu tìm thấy: {len(bridges)}\n"
                          f"T.Gian Thuật toán: {algo_time_ms:.4f} ms | T.Gian Animation: {anim_time_s:.2f} s")

    # 5. CHẠY KIỂM CHỨNG (VERIFICATION)
    verify_report = verify_bridges_with_bfs(G, bridges)
    for line in verify_report:
        txt_verify.insert(tk.END, line + "\n")
    txt_verify.config(state=tk.DISABLED)
    
    # Vẽ lại lần cuối kết quả hoàn chỉnh
    final_labels = {n: f"{n}\n({d}/{l})" for n, d, l, p in table_data}
    
    bridge_set = set(bridges) | set((v,u) for u,v in bridges)
    node_colors = ['#90EE90'] * len(G.nodes()) # Xanh lá (đã duyệt xong)
    edge_colors = ['red' if (u,v) in bridge_set else 'black' for u,v in G.edges()]
    
    update_canvas_step(G, pos, node_colors, edge_colors, final_labels, "KẾT QUẢ CUỐI CÙNG")


def clear_all():
    txt_input.delete("1.0", tk.END)
    lbl_stats.config(text="...")
    entry_vertices.delete(0, tk.END)
    
    widgets = [txt_log, txt_bridges_list, txt_verify]
    for w in widgets:
        w.config(state=tk.NORMAL)
        w.delete("1.0", tk.END)
        w.config(state=tk.DISABLED)
        
    for item in tree_table.get_children(): tree_table.delete(item)
    ax.clear(); ax.axis('off'); canvas.draw()

# --- HÀM TẠO DỮ LIỆU TEST (ĐẶT Ở NGOÀI MAIN) ---
def generate_test_data(num_nodes, num_edges):
    G_rand = nx.gnm_random_graph(num_nodes, num_edges, seed=42)
    edges_str = ""
    for u, v in G_rand.edges():
        edges_str += f"{u} {v}\n"
    return edges_str.strip()

# --- MAIN GUI ---
def main():
    global root, txt_input, lbl_stats, entry_vertices, ax, canvas 
    global txt_log, tree_table, txt_bridges_list, txt_verify

    root = tk.Tk()
    root.title("Advanced Bridge Finder: Visualization & Verification")
    root.geometry("1400x750")

    # --- KHUNG TRÁI: NHẬP LIỆU ---
    f_left = tk.Frame(root, width=200, bg="#f5f5f5", padx=5, pady=5)
    f_left.pack(side=tk.LEFT, fill=tk.Y)
    
    tk.Label(f_left, text="Số đỉnh(Tùy chọn nếu có đỉnh cô lập):", bg="#f5f5f5").pack(anchor="w")
    entry_vertices = tk.Entry(f_left); entry_vertices.pack(fill=tk.X)
    
    tk.Label(f_left, text="Danh sách cạnh:", bg="#f5f5f5").pack(anchor="w", pady=(10,0))
    txt_input = tk.Text(f_left, height=10, width=25); txt_input.pack(fill=tk.X)
    txt_input.insert(tk.END,generate_test_data(20, 42)) # Dữ liệu test mẫu
    
    btn_run = tk.Button(f_left, text="CHẠY (VISUALIZE)", command=start_processing, bg="green", fg="white", font=("Arial", 10, "bold"))
    btn_run.pack(fill=tk.X, pady=10)
    
    tk.Button(f_left, text="LÀM MỚI", command=clear_all, bg="orange", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X)
    lbl_stats = tk.Label(f_left, text="...", bg="#f5f5f5"); lbl_stats.pack(pady=10)

    # --- KHUNG GIỮA: ĐỒ THỊ + LIST CẦU ---
    f_mid = tk.Frame(root, bg="white", padx=5, pady=5)
    f_mid.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Canvas
    fig, ax = plt.subplots(figsize=(5,5))
    canvas = FigureCanvasTkAgg(fig, master=f_mid)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    ax.axis('off')
    
    # List cầu Output riêng
    tk.Label(f_mid, text="Danh sách Cầu tìm được:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
    txt_bridges_list = tk.Text(f_mid, height=5, bg="#ffebee")
    txt_bridges_list.pack(fill=tk.X)

    # --- KHUNG PHẢI: LOG + BẢNG + VERIFY ---
    f_right = tk.Frame(root, width=400, padx=5, pady=5)
    f_right.pack(side=tk.RIGHT, fill=tk.Y)

    # Bảng
    tk.Label(f_right, text="Bảng Disc/Low:", font=("Arial", 9, "bold")).pack(anchor="w")
    cols = ("V", "D", "L", "P")
    tree_table = ttk.Treeview(f_right, columns=cols, show="headings", height=6)
    for c in cols: tree_table.heading(c, text=c); tree_table.column(c, width=40, anchor="center")
    tree_table.pack(fill=tk.X)

    # Log Steps
    tk.Label(f_right, text="Các bước DFS:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5,0))
    txt_log = tk.Text(f_right, height=12, font=("Consolas", 8), bg="#FFF8DC")
    txt_log.pack(fill=tk.X)
    
    # Verification Report
    tk.Label(f_right, text="Kiểm chứng (Xóa cạnh & Check BFS):", font=("Arial", 9, "bold"), fg="blue").pack(anchor="w", pady=(10,0))
    txt_verify = tk.Text(f_right, height=10, font=("Consolas", 8), bg="#E0F7FA")
    txt_verify.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()