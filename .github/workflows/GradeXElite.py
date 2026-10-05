# -*- coding: utf-8 -*-
"""
GRADEX ELITE v8.0 - PHẦN MỀM QUẢN LÝ ĐIỂM SINH VIÊN
ĐH Bách khoa - ĐH Đà Nẵng | Lớp 26THXD1
Nhóm: Đỗ Thanh Phong (NT), Trần Trung Đỉnh,
      Nguyễn Phước Đạt, Trần Minh Trí
GVHD: Nguyễn Thanh Hải
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json, os, unicodedata, ctypes, random, math

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try: ctypes.windll.user32.SetProcessDPIAware()
    except Exception: pass

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

BUILD_DATE = "15/01/2026"
VERSION = "v8.0"

BK_BLUE, BK_YELLOW, BK_RED = "#0000CC", "#FFCC00", "#CC0000"
BK_WHITE, BK_NAVY, BK_LIGHT = "#FFFFFF", "#001A4D", "#F5F7FB"
HEADER_TOP, HEADER_BOT = "#001133", "#003399"

LOGO_FILE = "logo_bach_khoa.png"
LOGO_URL = ("https://cdn.haitrieu.com/wp-content/uploads/2021/10/"
            "Logo-Truong-Dai-hoc-Bach-khoa-Dai-hoc-Da-Nang-DUT.png")

_logo_cache = {}

def ensure_logo_downloaded():
    if os.path.exists(LOGO_FILE):
        return True
    if not (HAS_PIL and HAS_REQUESTS):
        return False
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0"}
        r = requests.get(LOGO_URL, headers=headers, timeout=10)
        r.raise_for_status()
        with open(LOGO_FILE, "wb") as f:
            f.write(r.content)
        return True
    except Exception:
        return False

def load_logo_photo(size):
    if size in _logo_cache:
        return _logo_cache[size]
    if not HAS_PIL: return None
    if not ensure_logo_downloaded(): return None
    try:
        img = Image.open(LOGO_FILE).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        _logo_cache[size] = photo
        return photo
    except Exception:
        return None

def make_school_logo(parent, size, bg):
    photo = load_logo_photo(size)
    if photo is not None:
        lbl = tk.Label(parent, image=photo, bg=bg, bd=0)
        lbl.image = photo
        return lbl
    c = tk.Canvas(parent, width=size, height=size, bg=bg, highlightthickness=0)
    draw_bk_logo_fallback(c, size, bg)
    return c

def draw_bk_logo_fallback(canvas, size, bg_color):
    canvas.delete("all")
    s = size
    canvas.create_rectangle(0,0,s,s, fill=bg_color, outline=BK_YELLOW, width=max(2, s//40))
    canvas.create_text(s*0.27, s*0.10, text="D", font=("Arial", int(s*0.14), "bold"),
                       fill=BK_BLUE, anchor="center")
    canvas.create_text(s*0.62, s*0.20, text="BẠCH KHOA",
                       font=("Arial", int(s*0.088), "bold"), fill=BK_RED, anchor="center")
    for i, ch in enumerate("NANG"):
        canvas.create_text(s*0.11, s*0.40 + i*s*0.145, text=ch,
                           font=("Arial", int(s*0.105), "bold"), fill=BK_BLUE, anchor="center")
    x1, y1, x2, y2 = s*0.24, s*0.32, s*0.96, s*0.96
    canvas.create_rectangle(x1, y1, x2, y2, fill=BK_YELLOW, outline=BK_YELLOW)
    ins = s*0.025
    bx1, by1, bx2, by2 = x1+ins, y1+ins, x2-ins, y2-ins
    canvas.create_rectangle(bx1, by1, bx2, by2, fill=BK_BLUE, outline=BK_BLUE)
    cw, ch = (bx2-bx1), (by2-by1)
    r = min(cw, ch)*0.42
    cx = bx2 - r - cw*0.02
    cy = (by1+by2)/2
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=BK_YELLOW, outline=BK_YELLOW)
    cx2 = cx - cw*0.15
    canvas.create_oval(cx2-r, cy-r, cx2+r, cy+r, fill=BK_BLUE, outline=BK_BLUE)

def draw_app_logo(canvas, size, bg_color="#FFFFFF"):
    canvas.delete("all")
    s = size
    cx, cy = s/2, s/2
    canvas.create_oval(1, 1, s-1, s-1, fill=BK_YELLOW, outline=BK_YELLOW)
    pad = max(3, s*0.06)
    canvas.create_oval(pad, pad, s-pad, s-pad, fill=BK_BLUE, outline=BK_NAVY, width=1)
    pad2 = pad + max(2, s*0.02)
    canvas.create_oval(pad2, pad2, s-pad2, s-pad2, fill=BK_BLUE, outline=BK_YELLOW, width=1)
    points = []
    for i in range(30):
        t = i / 29
        x = s*0.22 + t * s*0.56
        y = s*0.80 - t * s*0.60 + math.sin(t * math.pi) * s*0.10
        points.extend([x, y])
    if len(points) >= 4:
        canvas.create_line(*points, fill=BK_YELLOW, width=max(4, int(s*0.09)),
                           capstyle="round", smooth=True)
    canvas.create_polygon(s*0.72, s*0.20, s*0.78, s*0.24, s*0.82, s*0.18, s*0.76, s*0.14,
                          fill=BK_YELLOW, outline=BK_YELLOW)
    canvas.create_text(cx, cy - s*0.02, text="GX",
                       font=("Arial", int(s*0.32), "bold"), fill=BK_WHITE, anchor="center")
    canvas.create_line(s*0.32, cy + s*0.16, s*0.68, cy + s*0.16,
                       fill=BK_YELLOW, width=max(1, int(s*0.025)))
    canvas.create_text(cx, cy + s*0.24, text="ELITE",
                       font=("Arial", int(s*0.085), "bold"), fill=BK_YELLOW, anchor="center")

def draw_app_logo_at(canvas, x, y, size):
    """Vẽ logo GX tại vị trí (x,y) - dùng cho canvas có sẵn, KHÔNG xóa canvas"""
    s = size
    cx = x + s/2
    cy = y + s/2
    canvas.create_oval(x, y, x+s, y+s, fill=BK_YELLOW, outline=BK_YELLOW)
    pad = max(3, s*0.06)
    canvas.create_oval(x+pad, y+pad, x+s-pad, y+s-pad, fill=BK_BLUE, outline=BK_NAVY, width=1)
    pad2 = pad + max(2, s*0.02)
    canvas.create_oval(x+pad2, y+pad2, x+s-pad2, y+s-pad2, fill=BK_BLUE, outline=BK_YELLOW, width=1)
    points = []
    for i in range(30):
        t = i / 29
        px = x + s*0.22 + t * s*0.56
        py = y + s*0.80 - t * s*0.60 + math.sin(t * math.pi) * s*0.10
        points.extend([px, py])
    if len(points) >= 4:
        canvas.create_line(*points, fill=BK_YELLOW, width=max(4, int(s*0.09)),
                           capstyle="round", smooth=True)
    canvas.create_polygon(x+s*0.72, y+s*0.20, x+s*0.78, y+s*0.24,
                          x+s*0.82, y+s*0.18, x+s*0.76, y+s*0.14,
                          fill=BK_YELLOW, outline=BK_YELLOW)
    canvas.create_text(cx, cy - s*0.02, text="GX",
                       font=("Arial", int(s*0.32), "bold"), fill=BK_WHITE, anchor="center")
    canvas.create_line(x+s*0.32, cy + s*0.16, x+s*0.68, cy + s*0.16,
                       fill=BK_YELLOW, width=max(1, int(s*0.025)))
    canvas.create_text(cx, cy + s*0.24, text="ELITE",
                       font=("Arial", int(s*0.085), "bold"), fill=BK_YELLOW, anchor="center")

THEMES = {
    "light": {
        "bg": BK_LIGHT, "bg_alt": "#FFFFFF", "fg": "#0F172A", "fg_soft": "#64748B",
        "primary": BK_BLUE, "primary_light": "#2563EB",
        "accent": BK_YELLOW, "accent_dark": "#D4A000",
        "success": "#16A34A", "warning": "#F59E0B", "danger": BK_RED,
        "border": "#CBD5E0", "grid": "#94A3B8",
        "sidebar_bg": BK_NAVY, "sidebar_fg": "#E2E8F0", "sidebar_active": BK_BLUE,
        "topbar_bg": BK_WHITE, "card_bg": BK_WHITE,
        "footer_bg": BK_NAVY, "footer_fg": "#E2E8F0",
        "row_hover": "#E0ECFF",
    },
    "dark": {
        "bg": "#0A0E27", "bg_alt": "#141935", "fg": "#F8FAFC", "fg_soft": "#94A3B8",
        "primary": "#3B82F6", "primary_light": "#60A5FA",
        "accent": BK_YELLOW, "accent_dark": "#E6B800",
        "success": "#22C55E", "warning": "#FBBF24", "danger": "#EF4444",
        "border": "#2D3748", "grid": "#475569",
        "sidebar_bg": "#05070F", "sidebar_fg": "#E2E8F0", "sidebar_active": "#1E40AF",
        "topbar_bg": "#141935", "card_bg": "#141935",
        "footer_bg": "#05070F", "footer_fg": "#E2E8F0",
        "row_hover": "#1E2B4A",
    },
}
FONT_FAMILY = "Segoe UI"

CHUONG_TRINH_DAO_TAO = {
    "Học kỳ 1": [("Giải tích 1",4),("Vật lý Cơ và Nhiệt",3),("Thí nghiệm Vật lý",1),
                 ("Nhập môn ngành",2),("Triết học Mác - Lênin",3),("Hình họa - Vẽ kỹ thuật",3),
                 ("Nhập môn công nghệ số và ứng dụng trí tuệ nhân tạo",2)],
    "Học kỳ 2": [("Chủ nghĩa xã hội khoa học",2),("Giải tích 2 nâng cao",4),
                 ("Đại số tuyến tính",3),("Anh văn A2.2",4),("Ngôn ngữ lập trình trong xây dựng",2),
                 ("Hóa đại cương",2),("Cơ lý thuyết",2)],
    "Học kỳ 3": [("Lịch sử Đảng Cộng sản Việt Nam",2),("Cấu trúc và Cơ sở dữ liệu trong xây dựng",2),
                 ("Anh văn B1.1",3),("Phương pháp tính",2),("Sức bền vật liệu",3),
                 ("Thí nghiệm Sức bền vật liệu",0.5),("Trắc địa",2),("Thực tập trắc địa",1),
                 ("Thủy lực",2),("Thí nghiệm thủy lực",0.5)],
    "Học kỳ 4": [("Phân tích và thiết kế thuật toán trong xây dựng",2),
                 ("Kinh tế chính trị Mác - Lênin",2),("Ứng dụng xác suất và thống kê trong xây dựng",2),
                 ("Môi trường và phát triển bền vững",2),("Cơ học kết cấu 1",2),("Cơ học đất",2),
                 ("Thí nghiệm cơ học đất",0.5),("Vật liệu xây dựng",2),
                 ("Thí nghiệm Vật liệu xây dựng",0.5),("Thủy lực công trình",2)],
    "Học kỳ 5": [("Tư tưởng Hồ Chí Minh",2),("Thực hành lập trình MT, Windows",1),
                 ("Phương pháp Phần tử hữu hạn",2),("Phương pháp nghiên cứu khoa học",2),
                 ("Cơ học kết cấu 2",2),("Nền và móng",2),("Đồ án Nền và móng",1),
                 ("Kỹ thuật Bê tông cốt thép (phần cơ bản)",2),
                 ("Đồ án Kết cấu Bê tông cốt thép",1),("Thủy văn",2)],
    "Học kỳ 6": [("Pháp luật đại cương",2),("Tư duy khởi nghiệp và đổi mới sáng tạo",2),
                 ("Kỹ thuật điện và Điện tử",2),("Công trình thủy",2),("Đồ án Công trình thủy",1),
                 ("Cơ đất thiết kế kết cấu thép",2),("Phần mềm trong xây dựng",2),
                 ("Ứng dụng GIS trong xây dựng",2),("Thực tập hiện trường",1)],
    "Học kỳ 7": [("Phân tích phần tử môi trường",2),("Kỹ thuật thi công",3),
                 ("Kinh tế xây dựng",2),("Công nghệ BIM trong xây dựng",2),
                 ("Công trình giao thông",3),("PBL Thiết kế công trình giao thông",2),
                 ("PBL BIM trong thiết kế công trình",2)],
    "Học kỳ 8": [("Thiết kế tổng đường",2),("Thiết kế công trình thép",2),
                 ("Tổ chức thi công",2),("PBL Công nghệ BIM trong thi công",2),
                 ("Kỹ thuật hạ tầng cấp thoát nước",2),
                 ("PBL BIM trong thiết kế kết cấu hạ tầng",2),("Tự chọn (Chọn 2 học phần)",4)],
    "Học kỳ 9": [("Thực tập tốt nghiệp",8),("Đồ án tốt nghiệp",10)],
    "Môn Tự Chọn": [("Thủy văn công trình",2),("Mô hình toán thủy văn thủy lực",2),
                    ("Cấp thoát nước đô thị",2),("Thoát nước đô thị",2),
                    ("Mô hình toán ngập lụt đô thị",2),("Công trình ven biển",2),
                    ("Bê tông cốt thép dự ứng lực",2),("Thiết kế nền nhà thấp",2),
                    ("Quản lý dự án công trình xây dựng",2),("Quản lý doanh nghiệp xây dựng",2),
                    ("Công nghệ Bê tông siêu trọng lượng",2),("Trí tuệ nhân tạo trong xây dựng",2)],
    "Môn Bổ Sung": [("Tin học xây dựng",2)],
}
DANH_SACH_MON_PHANG = {t: tc for hk, ds in CHUONG_TRINH_DAO_TAO.items() for t, tc in ds}

LANG = {
    "vi": {
        "app_name":"GRADEX ELITE","app_sub":"Hệ thống Quản lý Điểm Sinh viên",
        "home":"Trang chủ","students":"Quản lý Sinh viên","program":"Chương trình đào tạo",
        "settings":"Cài đặt","about":"Giới thiệu",
        "welcome":"CHÀO MỪNG ĐẾN VỚI HỆ THỐNG","slogan":"Xây cơ sở - Dựng tương lai",
        "quick_access":"TRUY CẬP NHANH","stats":"THỐNG KÊ",
        "total_students":"Tổng sinh viên","total_subjects":"Tổng học phần",
        "total_credits":"Tổng tín chỉ","avg_score":"Điểm TB chung",
        "add_student":"Thêm Sinh viên","search_student":"Tìm kiếm sinh viên...",
        "student_name":"Tên sinh viên","student_list":"Danh sách sinh viên",
        "score_entry":"Bảng điểm của","back":"Quay lại",
        "search_subject":"Tìm kiếm học phần...",
        "subject":"Học phần","credits":"TC","process":"Quá trình (20%)",
        "midterm":"Giữa kỳ (20%)","final":"Cuối kỳ (60%)",
        "avg":"Điểm TB","rank":"Xếp loại","gpa":"GPA",
        "language":"Ngôn ngữ","theme":"Giao diện","light":"Sáng","dark":"Tối",
        "saved":"Đã lưu dữ liệu!","loaded":"Đã tải dữ liệu!",
        "export":"Xuất dữ liệu","import":"Nhập dữ liệu","delete":"Xóa","edit":"Sửa",
        "empty_warning":"Vui lòng nhập đầy đủ thông tin!","dup_warning":"Sinh viên đã tồn tại!",
        "score_range_warning":"Điểm phải nằm trong khoảng 0 - 10!",
        "group":"Nhóm thực hiện","instructor":"GVHD","class":"Lớp",
        "university":"Trường Đại học Bách khoa - Đại học Đà Nẵng",
        "faculty":"Khoa Xây dựng","program_name":"Ngành Tin học Xây dựng",
        "about_title":"GIỚI THIỆU PHẦN MỀM","team":"ĐỘI NGŨ PHÁT TRIỂN",
        "tech":"CÔNG NGHỆ SỬ DỤNG","features":"TÍNH NĂNG NỔI BẬT",
        "stt":"STT","n_subjects":"Số môn","action":"Hành động",
        "language_vi":"Tiếng Việt","language_en":"Tiếng Anh",
        "font_size":"Cỡ chữ","sound":"Âm thanh","notify":"Thông báo","autosave":"Tự động lưu",
        "on":"Bật","off":"Tắt","data_management":"Quản lý dữ liệu",
        "notifications":"Thông báo & Âm thanh",
        "edit_student":"Sửa tên sinh viên","new_name":"Tên mới",
        "delete_student_confirm":"Bạn có chắc muốn xóa sinh viên này?",
        "score_hint":"Nhập đủ 3 cột để tính điểm TB",
        "welcome_user":"Chào mừng","leader":"Nhóm trưởng","member":"Thành viên",
        "app_desc":"GradeX Elite là phần mềm quản lý điểm dành cho sinh viên, được phát triển bởi nhóm sinh viên lớp 26THXD1. Phần mềm giúp nhập, tính điểm tự động theo trọng số 20% - 20% - 60%, quy đổi thang điểm 4, xếp loại học lực và quản lý danh sách sinh viên một cách trực quan.",
        "build_date":"Ngày xây dựng",
    },
    "en": {
        "app_name":"GRADEX ELITE","app_sub":"Student Grade Management System",
        "home":"Home","students":"Students","program":"Curriculum",
        "settings":"Settings","about":"About",
        "welcome":"WELCOME TO THE SYSTEM","slogan":"Build the Foundation - Construct the Future",
        "quick_access":"QUICK ACCESS","stats":"STATISTICS",
        "total_students":"Total Students","total_subjects":"Total Subjects",
        "total_credits":"Total Credits","avg_score":"Overall GPA",
        "add_student":"Add Student","search_student":"Search student...",
        "student_name":"Student Name","student_list":"Student List",
        "score_entry":"Score Sheet of","back":"Back",
        "search_subject":"Search subject...",
        "subject":"Subject","credits":"Cr.","process":"Process (20%)",
        "midterm":"Midterm (20%)","final":"Final (60%)",
        "avg":"Average","rank":"Rank","gpa":"GPA",
        "language":"Language","theme":"Theme","light":"Light","dark":"Dark",
        "saved":"Saved!","loaded":"Loaded!",
        "export":"Export","import":"Import","delete":"Delete","edit":"Edit",
        "empty_warning":"Please fill in all required fields!","dup_warning":"Student already exists!",
        "score_range_warning":"Score must be between 0 and 10!",
        "group":"Development Team","instructor":"Instructor","class":"Class",
        "university":"Danang University of Science and Technology",
        "faculty":"Faculty of Construction","program_name":"Civil Informatics Program",
        "about_title":"ABOUT THE SOFTWARE","team":"DEVELOPMENT TEAM",
        "tech":"TECHNOLOGIES","features":"KEY FEATURES",
        "stt":"No.","n_subjects":"Subjects","action":"Action",
        "language_vi":"Vietnamese","language_en":"English",
        "font_size":"Font size","sound":"Sound","notify":"Notifications","autosave":"Auto save",
        "on":"On","off":"Off","data_management":"Data Management",
        "notifications":"Notifications & Sound",
        "edit_student":"Edit student name","new_name":"New name",
        "delete_student_confirm":"Are you sure you want to delete this student?",
        "score_hint":"Fill all 3 columns to compute average",
        "welcome_user":"Welcome","leader":"Leader","member":"Member",
        "app_desc":"GradeX Elite is a grade management application for students, developed by the 26THXD1 class team. It allows users to enter and compute scores (20% - 20% - 60%), convert to 4.0 scale, rank students, and manage student lists intuitively.",
        "build_date":"Build date",
    }
}

def capitalize_name(name):
    return " ".join(w.capitalize() for w in name.split())

def sort_key_vietnamese(name):
    name = name.strip().lower()
    n = unicodedata.normalize("NFD", name)
    n = "".join(ch for ch in n if unicodedata.category(ch) != "Mn")
    return n


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)
        self.scrollable_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self._win_id = self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_wheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_canvas_resize(self, e):
        self.canvas.itemconfig(self._win_id, width=e.width)

    def _on_wheel(self, ev):
        try: self.canvas.yview_scroll(int(-1*(ev.delta/120)), "units")
        except Exception: pass


class GradeXEliteApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"GradeX Elite {VERSION} - ĐH Bách khoa Đà Nẵng")

        # === TỰ ĐỘNG ĐIỀU CHỈNH KÍCH THƯỚC CỬA SỔ THEO MÀN HÌNH ===
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        # Lấy 92% màn hình, không vượt quá 1600x1000
        win_w = min(int(sw * 0.92), 1600)
        win_h = min(int(sh * 0.92), 1000)
        # Đảm bảo tối thiểu
        win_w = max(win_w, 1100)
        win_h = max(win_h, 700)
        x = (sw - win_w) // 2
        y = max(0, (sh - win_h) // 2 - 20)
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.root.minsize(1050, 650)

        self.theme, self.lang, self.current_page = "light", "vi", "home"
        self.students, self.current_student = [], None
        self.settings = {"font_scale":1.0, "sound_on":True, "notify_on":True}
        self.data_file = os.path.join(os.path.expanduser("~"), "gradex_elite_v8.json")
        self._header_redraw_job = None
        ensure_logo_downloaded()
        self.apply_theme()
        self.show_splash()

    def t(self, k): return LANG[self.lang].get(k, k)
    def c(self, k): return THEMES[self.theme].get(k, "#000")
    def fs(self, b, e=0): return int((b+e) * self.settings["font_scale"])

    def apply_theme(self):
        c = THEMES[self.theme]
        self.root.configure(bg=c["bg"])
        st = ttk.Style()
        try: st.theme_use("clam")
        except Exception: pass
        st.configure("Treeview", background=c["card_bg"], foreground=c["fg"],
                     fieldbackground=c["card_bg"], rowheight=38,
                     font=(FONT_FAMILY, self.fs(11)), borderwidth=1, relief="solid")
        st.map("Treeview", background=[("selected", c["primary_light"])], foreground=[("selected","white")])
        st.configure("Treeview.Heading", background=c["primary"], foreground="white",
                     font=(FONT_FAMILY, self.fs(11), "bold"), borderwidth=1, relief="solid")
        st.configure("TProgressbar", troughcolor=c["bg_alt"], background=c["primary"])

    def beep(self, kind):
        if not HAS_SOUND or not self.settings["sound_on"]: return
        try:
            if kind=="start": winsound.Beep(880,100); winsound.Beep(1320,150)
            elif kind=="success": winsound.Beep(1000,100)
            elif kind=="excellent": [winsound.Beep(f,90) for f in (1200,1500,1800)]
            elif kind=="good": winsound.Beep(1200,120)
            elif kind=="ok": winsound.Beep(900,100)
            elif kind=="meh": winsound.Beep(700,100)
            elif kind=="bad": winsound.Beep(400,200); winsound.Beep(300,200)
        except Exception: pass

    # ============ SPLASH ============
    def show_splash(self):
        sp = tk.Toplevel()
        sp.overrideredirect(True); sp.configure(bg=BK_WHITE)
        w, h = 720, 580
        sw, sh = sp.winfo_screenwidth(), sp.winfo_screenheight()
        sp.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        br = tk.Frame(sp, bg=BK_YELLOW); br.pack(fill="both", expand=True, padx=6, pady=6)
        inner = tk.Frame(br, bg=BK_WHITE); inner.pack(fill="both", expand=True, padx=4, pady=4)
        logos = tk.Frame(inner, bg=BK_WHITE); logos.pack(pady=(15,5))
        sc_frame = tk.Frame(logos, bg=BK_WHITE)
        sc_frame.pack(side="left", padx=15)
        make_school_logo(sc_frame, 120, BK_WHITE).pack()
        ac = tk.Canvas(logos, width=120, height=120, bg=BK_WHITE, highlightthickness=0)
        ac.pack(side="left", padx=15); draw_app_logo(ac, 120)
        tk.Label(inner, text="ĐẠI HỌC BÁCH KHOA", font=(FONT_FAMILY,16,"bold"),
                 bg=BK_WHITE, fg=BK_BLUE).pack()
        tk.Label(inner, text="ĐẠI HỌC ĐÀ NẴNG", font=(FONT_FAMILY,11),
                 bg=BK_WHITE, fg=BK_RED).pack()
        tk.Frame(inner, bg=BK_YELLOW, height=3, width=500).pack(pady=10)
        tk.Label(inner, text="GRADEX ELITE", font=("Segoe UI",26,"bold"),
                 bg=BK_WHITE, fg=BK_BLUE).pack()
        tk.Label(inner, text=self.t("app_sub"), font=(FONT_FAMILY,11,"italic"),
                 bg=BK_WHITE, fg=BK_NAVY).pack(pady=(3,10))
        tk.Label(inner, text=f"{self.t('group')}:", font=(FONT_FAMILY,10,"italic"),
                 bg=BK_WHITE, fg="#666").pack()
        tk.Label(inner, text="Đỗ Thanh Phong  •  Trần Trung Đỉnh  •  Nguyễn Phước Đạt  •  Trần Minh Trí",
                 font=(FONT_FAMILY,10,"bold"), bg=BK_WHITE, fg=BK_BLUE).pack(pady=(3,8))
        tk.Label(inner, text=f"{self.t('instructor')}: Nguyễn Thanh Hải",
                 font=(FONT_FAMILY,11,"bold"), bg=BK_WHITE, fg=BK_RED).pack()
        tk.Label(inner, text=f"{self.t('build_date')}: {BUILD_DATE}",
                 font=(FONT_FAMILY,9), bg=BK_WHITE, fg="#666").pack(pady=(5,0))
        pb = ttk.Progressbar(inner, orient="horizontal", length=500, mode="indeterminate")
        pb.pack(pady=12); pb.start(12)
        self.beep("start")
        sp.after(3500, lambda: (sp.destroy(), self.build_main_ui()))

    # ============ MAIN LAYOUT ============
    def build_main_ui(self):
        for w in self.root.winfo_children(): w.destroy()
        self.sidebar = tk.Frame(self.root, bg=self.c("sidebar_bg"), width=260)
        self.sidebar.pack(side="left", fill="y"); self.sidebar.pack_propagate(False)
        self.right = tk.Frame(self.root, bg=self.c("bg"))
        self.right.pack(side="right", fill="both", expand=True)
        self.build_header()
        self.footer = self.build_footer(self.right)
        self.content = tk.Frame(self.right, bg=self.c("bg"))
        self.content.pack(fill="both", expand=True)
        self.build_sidebar()
        self.load_data()
        self.show_home()

    # ============ HEADER (RESPONSIVE - VẼ LẠI KHI RESIZE) ============
    def build_header(self):
        self.header_h = int(150 * max(1.0, self.settings["font_scale"]))
        self.header_canvas = tk.Canvas(self.right, height=self.header_h,
                                       bg=HEADER_TOP, highlightthickness=0, bd=0)
        self.header_canvas.pack(fill="x")
        # Bind sự kiện resize -> vẽ lại
        self.header_canvas.bind("<Configure>", self._on_header_resize)
        # Vẽ lần đầu
        self.root.after(50, self._redraw_header)

    def _on_header_resize(self, event):
        """Debounce: chờ 30ms rồi mới vẽ lại để tránh lag"""
        if self._header_redraw_job:
            self.root.after_cancel(self._header_redraw_job)
        self._header_redraw_job = self.root.after(30, self._redraw_header)

    def _redraw_header(self):
        """Vẽ lại toàn bộ header dựa trên kích thước canvas hiện tại"""
        if not hasattr(self, "header_canvas"): return
        try:
            W = self.header_canvas.winfo_width()
            H = self.header_canvas.winfo_height()
        except Exception:
            return
        if W < 50 or H < 30: return

        self.header_canvas.delete("all")

        # Gradient nền
        for i in range(H):
            t = i / max(1, H-1)
            g = int(0x11 + (0x33 - 0x11) * t)
            b = int(0x33 + (0x99 - 0x33) * t)
            self.header_canvas.create_line(0, i, W, i, fill=f"#00{g:02x}{b:02x}")

        # Họa tiết mạch (số lượng tỉ lệ theo W)
        n_lines = max(20, W // 30)
        for _ in range(n_lines):
            x1 = random.randint(0, W); y1 = random.randint(0, H)
            x2 = x1 + random.randint(20, 80); y2 = y1 + random.choice([0, 30])
            self.header_canvas.create_line(x1, y1, x2, y2, fill="#1a4a99", width=1)
        for i in range(0, W, 60):
            x = i + random.randint(-10, 10)
            self.header_canvas.create_line(x, H-20, x, H, fill="#0a2a66", width=2)
        self.header_canvas.create_oval(W//2-350, -100, W//2+350, 250,
                                        fill="", outline="#1a4a99", width=1)
        self.header_canvas.create_oval(W//2-250, -50, W//2+250, 200,
                                        fill="", outline="#2563eb", width=1)

        cy_main = H // 2

        # ==== LOGO TRƯỜNG BÊN TRÁI ====
        # (dùng ảnh thật qua make_school_logo)
        logo_sch_size = int(H * 0.62)
        lf = tk.Frame(self.header_canvas, bg=HEADER_TOP)
        self.header_canvas.create_window(80, cy_main, window=lf, anchor="center",
                                          width=logo_sch_size, height=logo_sch_size)
        # Xóa frame cũ trong lf (nếu có) để vẽ mới
        for w in lf.winfo_children(): w.destroy()
        make_school_logo(lf, logo_sch_size, HEADER_TOP).pack()

        # ==== TÊN TRƯỜNG ====
        tx = int(logo_sch_size * 1.55) if logo_sch_size else 130
        fs_main = max(8, int(12 * self.settings["font_scale"]))
        fs_sub = max(7, int(9 * self.settings["font_scale"]))
        self.header_canvas.create_text(tx, cy_main - int(H*0.22),
            text="TRƯỜNG ĐẠI HỌC BÁCH KHOA",
            font=(FONT_FAMILY, fs_main, "bold"), fill="white", anchor="w")
        self.header_canvas.create_text(tx, cy_main - int(H*0.05),
            text="ĐẠI HỌC ĐÀ NẴNG • LỚP 26THXD1",
            font=(FONT_FAMILY, fs_sub), fill="#A9C4E4", anchor="w")
        self.header_canvas.create_text(tx, cy_main + int(H*0.12),
            text="Khoa Xây dựng • Ngành Tin học Xây dựng",
            font=(FONT_FAMILY, fs_sub), fill="#7FA9D9", anchor="w")

        # ==== LOGO GX BÊN PHẢI ====
        logo_sz = int(H * 0.62)
        right_pad = 30
        logo_x = W - right_pad - logo_sz
        logo_y = cy_main - logo_sz // 2
        if logo_x > tx + 200:  # chỉ vẽ nếu đủ chỗ
            draw_app_logo_at(self.header_canvas, logo_x, logo_y, logo_sz)

            # Tên app bên trái logo
            rx = logo_x - 20
            fs_app = max(10, int(20 * self.settings["font_scale"]))
            self.header_canvas.create_text(rx, cy_main - int(H*0.10),
                text="GRADEX ELITE",
                font=(FONT_FAMILY, fs_app, "bold"), fill=BK_YELLOW, anchor="e")
            self.header_canvas.create_text(rx, cy_main + int(H*0.10),
                text=self.t("app_sub"),
                font=(FONT_FAMILY, max(7, int(10*self.settings["font_scale"])), "italic"),
                fill="white", anchor="e")

    # ============ SIDEBAR ============
    def build_sidebar(self):
        c = THEMES[self.theme]
        for w in self.sidebar.winfo_children(): w.destroy()
        logo_box = tk.Frame(self.sidebar, bg=c["sidebar_bg"], pady=20)
        logo_box.pack(fill="x")
        lc = tk.Canvas(logo_box, width=80, height=80, bg=c["sidebar_bg"], highlightthickness=0)
        lc.pack(); draw_app_logo(lc, 80)
        tk.Label(logo_box, text="GRADEX ELITE", font=(FONT_FAMILY,14,"bold"),
                 bg=c["sidebar_bg"], fg=c["accent"]).pack(pady=(10,0))
        tk.Frame(self.sidebar, bg=c["accent"], height=2).pack(fill="x", padx=15, pady=8)
        info = tk.Frame(self.sidebar, bg=c["sidebar_bg"], padx=20); info.pack(fill="x")
        tk.Label(info, text=f"👤  {self.t('class')}: 26THXD1", font=(FONT_FAMILY,11,"bold"),
                 bg=c["sidebar_bg"], fg=c["accent"], anchor="w").pack(fill="x")
        tk.Label(info, text=f"     {self.t('program_name')}", font=(FONT_FAMILY,10),
                 bg=c["sidebar_bg"], fg="#A9C4E4", anchor="w").pack(fill="x")
        tk.Frame(self.sidebar, bg=c["accent"], height=1).pack(fill="x", padx=15, pady=10)
        menu = tk.Frame(self.sidebar, bg=c["sidebar_bg"]); menu.pack(fill="x")
        items = [("home","🏠",self.t("home"),self.show_home),
                 ("students","👨‍🎓",self.t("students"),self.show_students),
                 ("program","📚",self.t("program"),self.show_program),
                 ("settings","⚙️",self.t("settings"),self.show_settings),
                 ("about","ℹ️",self.t("about"),self.show_about)]
        self.menu_buttons = {}
        for key, icon, label, cmd in items:
            active = (self.current_page == key)
            btn = tk.Button(menu, text=f"  {icon}   {label}",
                font=(FONT_FAMILY, 11, "bold" if active else "normal"),
                bg=c["sidebar_active"] if active else c["sidebar_bg"],
                fg="white" if active else c["sidebar_fg"],
                activebackground=c["primary_light"], activeforeground="white",
                bd=0, anchor="w", padx=20, pady=14, cursor="hand2",
                command=lambda k=key, f=cmd: self.navigate(k, f))
            btn.pack(fill="x", pady=1)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=c["primary_light"]))
            btn.bind("<Leave>", lambda e, b=btn, k=key: b.config(
                bg=c["sidebar_active"] if self.current_page==k else c["sidebar_bg"]))
            self.menu_buttons[key] = btn
        bt = tk.Frame(self.sidebar, bg=c["sidebar_bg"])
        bt.pack(side="bottom", fill="x", pady=15, padx=15)
        tk.Frame(bt, bg=c["accent"], height=1).pack(fill="x", pady=(0,10))
        tk.Label(bt, text=f"Phiên bản {VERSION}", font=(FONT_FAMILY,9),
                 bg=c["sidebar_bg"], fg="#A9C4E4").pack()
        tk.Label(bt, text=f"Xây dựng: {BUILD_DATE}", font=(FONT_FAMILY,8),
                 bg=c["sidebar_bg"], fg="#7FA9D9").pack()
        tk.Label(bt, text="© 2026 - 26THXD1", font=(FONT_FAMILY,8),
                 bg=c["sidebar_bg"], fg="#A9C4E4").pack()

    def navigate(self, key, func):
        self.current_page = key
        c = THEMES[self.theme]
        for k, b in self.menu_buttons.items():
            active = (k==key)
            b.config(bg=c["sidebar_active"] if active else c["sidebar_bg"],
                     font=(FONT_FAMILY,11,"bold" if active else "normal"))
        func()

    # ============ FOOTER ============
    def build_footer(self, parent):
        c = THEMES[self.theme]
        footer = tk.Frame(parent, bg=c["footer_bg"], height=95)
        footer.pack(fill="x", side="bottom"); footer.pack_propagate(False)
        tk.Frame(footer, bg=c["accent"], height=3).pack(fill="x")
        inner = tk.Frame(footer, bg=c["footer_bg"]); inner.pack(fill="both", expand=True, padx=25, pady=10)
        col1 = tk.Frame(inner, bg=c["footer_bg"]); col1.pack(side="left", fill="y")
        tk.Label(col1, text=f"🎓 {self.t('university')}", font=(FONT_FAMILY,10,"bold"),
                 bg=c["footer_bg"], fg="white", anchor="w").pack(anchor="w")
        tk.Label(col1, text=f"    {self.t('faculty')} - {self.t('program_name')}",
                 font=(FONT_FAMILY,9), bg=c["footer_bg"], fg="#A9C4E4", anchor="w").pack(anchor="w")
        tk.Label(col1, text=f"    {self.t('build_date')}: {BUILD_DATE}",
                 font=(FONT_FAMILY,9), bg=c["footer_bg"], fg="#7FA9D9", anchor="w").pack(anchor="w")
        col2 = tk.Frame(inner, bg=c["footer_bg"]); col2.pack(side="left", fill="y", padx=40)
        tk.Label(col2, text=f"👥 {self.t('group')}:", font=(FONT_FAMILY,10,"bold"),
                 bg=c["footer_bg"], fg=c["accent"], anchor="w").pack(anchor="w")
        tk.Label(col2, text="Đỗ Thanh Phong • Trần Trung Đỉnh • Nguyễn Phước Đạt • Trần Minh Trí",
                 font=(FONT_FAMILY,9), bg=c["footer_bg"], fg="white", anchor="w").pack(anchor="w")
        col3 = tk.Frame(inner, bg=c["footer_bg"]); col3.pack(side="right", fill="y")
        tk.Label(col3, text=f"👨‍🏫 {self.t('instructor')}: Nguyễn Thanh Hải",
                 font=(FONT_FAMILY,10,"bold"), bg=c["footer_bg"], fg=c["accent"], anchor="e").pack(anchor="e")
        tk.Label(col3, text=f"© 2026 GRADEX ELITE {VERSION}",
                 font=(FONT_FAMILY,9), bg=c["footer_bg"], fg="white", anchor="e").pack(anchor="e")
        return footer

    def clear_content(self):
        for w in self.content.winfo_children(): w.destroy()

    def fade_in_content(self):
        try:
            self.root.attributes("-alpha", 0.85)
            for i in range(3):
                self.root.after(i*60, lambda a=0.88+0.04*i: self.root.attributes("-alpha", a))
            self.root.after(220, lambda: self.root.attributes("-alpha", 1.0))
        except Exception: pass

    # ============ HOME ============
    def show_home(self):
        self.clear_content()
        c = THEMES[self.theme]
        scroll = ScrollableFrame(self.content, bg=c["bg"])
        scroll.pack(fill="both", expand=True)
        parent = scroll.scrollable_frame

        sf = tk.Frame(parent, bg=c["bg"]); sf.pack(fill="x", padx=40, pady=(25, 10))
        tk.Label(sf, text="📊  " + self.t("stats"),
                 font=(FONT_FAMILY, self.fs(16), "bold"),
                 bg=c["bg"], fg=c["primary"]).pack(anchor="w", pady=(0,12))
        cf = tk.Frame(sf, bg=c["bg"]); cf.pack(fill="x")
        total_s, total_subj = len(self.students), len(DANH_SACH_MON_PHANG)
        total_cr = sum(DANH_SACH_MON_PHANG.values())
        avg = 0
        if self.students:
            gs = [self.calc_gpa(s)[0] for s in self.students]
            gs = [g for g in gs if g > 0]
            if gs: avg = sum(gs)/len(gs)
        for icon, lbl, val, col in [
            ("👨‍🎓", self.t("total_students"), str(total_s), c["primary"]),
            ("📚", self.t("total_subjects"), str(total_subj), c["success"]),
            ("🎯", self.t("total_credits"), str(int(total_cr)), c["accent_dark"]),
            ("🏆", self.t("avg_score"), f"{avg:.2f}" if avg else "—", c["danger"])]:
            card = tk.Frame(cf, bg=c["card_bg"],
                            highlightbackground=c["border"], highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=8, ipady=15)
            tk.Label(card, text=icon, font=("Segoe UI", 28), bg=c["card_bg"], fg=col).pack(pady=(10,5))
            tk.Label(card, text=val, font=("Segoe UI", self.fs(22), "bold"),
                     bg=c["card_bg"], fg=c["primary"]).pack()
            tk.Label(card, text=lbl, font=(FONT_FAMILY, self.fs(10)),
                     bg=c["card_bg"], fg=c["fg_soft"], wraplength=200).pack(pady=(3,10))

        qf = tk.Frame(parent, bg=c["bg"]); qf.pack(fill="x", padx=40, pady=(20, 20))
        tk.Label(qf, text="🚀  " + self.t("quick_access"),
                 font=(FONT_FAMILY, self.fs(16), "bold"),
                 bg=c["bg"], fg=c["primary"]).pack(anchor="w", pady=(0,12))

        cards_data = [
            ("👨‍🎓", self.t("students"), "Quản lý danh sách sinh viên, nhập và theo dõi điểm",
             self.show_students, c["primary"]),
            ("📚", self.t("program"), "Xem toàn bộ chương trình đào tạo theo từng học kỳ",
             self.show_program, c["success"]),
            ("⚙️", self.t("settings"), "Tùy chỉnh giao diện, ngôn ngữ và các thiết lập khác",
             self.show_settings, c["warning"]),
            ("ℹ️", self.t("about"), "Tìm hiểu về phần mềm và đội ngũ phát triển",
             self.show_about, c["danger"]),
        ]
        card_h = int(140 * max(1.0, self.settings["font_scale"]))
        container = tk.Frame(qf, bg=c["bg"], height=card_h*2 + 30)
        container.pack(fill="x")
        container.pack_propagate(False)

        def make_card(idx, icon, title, desc, cmd, color):
            row, col = idx // 2, idx % 2
            base_x = col*0.5 + 0.01
            base_y = row*0.5 + 0.01
            base_w = 0.48
            base_h = 0.48

            card = tk.Frame(container, bg=c["card_bg"],
                            highlightbackground=c["border"], highlightthickness=1)
            card.place(relx=base_x, rely=base_y, relwidth=base_w, relheight=base_h)

            inner = tk.Frame(card, bg=c["card_bg"])
            inner.pack(fill="both", expand=True, padx=20, pady=15)
            tk.Label(inner, text=icon, font=("Segoe UI", 32),
                     bg=c["card_bg"], fg=color).pack(side="left", padx=(0,15))
            tb = tk.Frame(inner, bg=c["card_bg"]); tb.pack(side="left", fill="both", expand=True)
            tk.Label(tb, text=title, font=(FONT_FAMILY, self.fs(15), "bold"),
                     bg=c["card_bg"], fg=c["primary"], anchor="w").pack(anchor="w")
            tk.Label(tb, text=desc, font=(FONT_FAMILY, self.fs(10)),
                     bg=c["card_bg"], fg=c["fg_soft"], anchor="w",
                     wraplength=400, justify="left").pack(anchor="w")

            def on_enter(e):
                card.place_configure(
                    relx=base_x - 0.008, rely=base_y - 0.008,
                    relwidth=base_w + 0.016, relheight=base_h + 0.016)
                card.config(highlightbackground=color, highlightthickness=2)

            def on_leave(e):
                card.place_configure(
                    relx=base_x, rely=base_y,
                    relwidth=base_w, relheight=base_h)
                card.config(highlightbackground=c["border"], highlightthickness=1)

            def on_click(e):
                self.navigate(self._page_key(cmd), cmd); self.fade_in_content()

            def bind_recursive(w):
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)
                w.bind("<Button-1>", on_click)
                for ch in w.winfo_children(): bind_recursive(ch)

            bind_recursive(card)

        for i, (icon, title, desc, cmd, color) in enumerate(cards_data):
            make_card(i, icon, title, desc, cmd, color)

        tk.Frame(parent, bg=c["bg"], height=30).pack()

    def _page_key(self, func):
        return {self.show_home:"home", self.show_students:"students",
                self.show_program:"program", self.show_settings:"settings",
                self.show_about:"about"}.get(func, "home")

    # ============ QUẢN LÝ SINH VIÊN ============
    def show_students(self):
        self.clear_content()
        c = THEMES[self.theme]
        head = tk.Frame(self.content, bg=c["bg"], pady=15); head.pack(fill="x", padx=40)
        tk.Label(head, text="👨‍🎓  " + self.t("students"),
                 font=(FONT_FAMILY, self.fs(24), "bold"),
                 bg=c["bg"], fg=c["primary"]).pack(anchor="w")
        tk.Label(head, text="Nhấp vào tên để mở bảng điểm • Nút ✏️ sửa tên • Nút ✖ xóa",
                 font=(FONT_FAMILY, self.fs(10)), bg=c["bg"], fg=c["fg_soft"]).pack(anchor="w")

        tb = tk.Frame(self.content, bg=c["card_bg"],
                      highlightbackground=c["grid"], highlightthickness=1)
        tb.pack(fill="x", padx=40, pady=10, ipady=15)
        inner = tk.Frame(tb, bg=c["card_bg"]); inner.pack(fill="x", padx=20)
        tk.Label(inner, text=f"{self.t('student_name')}:", font=(FONT_FAMILY, self.fs(11)),
                 bg=c["card_bg"], fg=c["fg"]).pack(side="left", padx=(0,8))
        self.ent_name = ttk.Entry(inner, width=30, font=(FONT_FAMILY, self.fs(11)))
        self.ent_name.pack(side="left", ipady=5, padx=5)
        self.ent_name.bind("<Return>", lambda e: self.add_student())
        tk.Button(inner, text="➕  " + self.t("add_student"),
                  font=(FONT_FAMILY, self.fs(10), "bold"), bg=c["success"], fg="white",
                  bd=0, padx=15, pady=8, cursor="hand2",
                  command=self.add_student).pack(side="left", padx=10)
        tk.Label(inner, text="🔍", font=(FONT_FAMILY, 12),
                 bg=c["card_bg"], fg=c["fg"]).pack(side="left", padx=(30,5))
        self.ent_search = ttk.Entry(inner, width=25, font=(FONT_FAMILY, self.fs(11)))
        self.ent_search.pack(side="left", ipady=5)
        self._search_after = None
        self.ent_search.bind("<KeyRelease>", self._on_search_debounce)

        list_head = tk.Frame(self.content, bg=c["bg"]); list_head.pack(fill="x", padx=40, pady=(15,5))
        self.lbl_list_title = tk.Label(list_head,
            text=f"📋  {self.t('student_list')} ({len(self.students)})",
            font=(FONT_FAMILY, self.fs(14), "bold"), bg=c["bg"], fg=c["primary"])
        self.lbl_list_title.pack(anchor="w")

        table_wrap = tk.Frame(self.content, bg=c["card_bg"],
                              highlightbackground=c["grid"], highlightthickness=2)
        table_wrap.pack(fill="both", expand=True, padx=40, pady=(5,20))

        hdr = tk.Frame(table_wrap, bg=c["primary"]); hdr.pack(fill="x")
        tk.Label(hdr, text="STT", font=(FONT_FAMILY, self.fs(11), "bold"),
                 bg=c["primary"], fg="white", width=6, pady=10).pack(side="left")
        tk.Label(hdr, text=self.t("student_name"), font=(FONT_FAMILY, self.fs(11), "bold"),
                 bg=c["primary"], fg="white", anchor="w", padx=10, pady=10
                 ).pack(side="left", fill="x", expand=True)
        for txt, w in [(self.t("n_subjects"),10),(self.t("gpa"),10),
                       (self.t("rank"),12),(self.t("action"),14)]:
            tk.Label(hdr, text=txt, font=(FONT_FAMILY, self.fs(11), "bold"),
                     bg=c["primary"], fg="white", width=w, pady=10).pack(side="left")

        self.sv_scroll = ScrollableFrame(table_wrap, bg=c["card_bg"])
        self.sv_scroll.pack(fill="both", expand=True)
        self.refresh_student_list()

    def _on_search_debounce(self, e=None):
        if self._search_after: self.root.after_cancel(self._search_after)
        self._search_after = self.root.after(250, self.refresh_student_list)

    def refresh_student_list(self):
        c = THEMES[self.theme]
        parent = self.sv_scroll.scrollable_frame
        for w in parent.winfo_children(): w.destroy()
        self.students.sort(key=lambda s: sort_key_vietnamese(s["name"]))
        kw = self.ent_search.get().strip().lower() if hasattr(self, "ent_search") else ""
        cnt = 0
        for i, s in enumerate(self.students, 1):
            if kw and kw not in s["name"].lower(): continue
            scores = s.get("scores", {})
            n_subj = len([k for k,v in scores.items() if v.get("tb","") != ""])
            gpa, rank = self.calc_gpa(s)
            gpa_str = f"{gpa:.2f}" if gpa > 0 else "—"
            bg = c["card_bg"] if cnt % 2 == 0 else c["bg_alt"]
            self._make_student_row(parent, i, s, n_subj, gpa_str, rank, bg)
            cnt += 1
        if hasattr(self, "lbl_list_title"):
            self.lbl_list_title.config(text=f"📋  {self.t('student_list')} ({len(self.students)})")

    def _make_student_row(self, parent, stt, s, n_subj, gpa_str, rank, bg):
        c = THEMES[self.theme]
        row = tk.Frame(parent, bg=bg, highlightbackground=c["grid"], highlightthickness=1)
        row.pack(fill="x", pady=1)
        tk.Label(row, text=str(stt), font=(FONT_FAMILY, self.fs(11)),
                 bg=bg, fg=c["fg"], width=6, pady=10).pack(side="left")
        name_lbl = tk.Label(row, text=s["name"], font=(FONT_FAMILY, self.fs(11), "bold"),
                            bg=bg, fg=c["primary"], anchor="w", padx=10, pady=10, cursor="hand2")
        name_lbl.pack(side="left", fill="x", expand=True)
        tk.Label(row, text=str(n_subj), font=(FONT_FAMILY, self.fs(11)),
                 bg=bg, fg=c["fg"], width=10, pady=10).pack(side="left")
        tk.Label(row, text=gpa_str, font=(FONT_FAMILY, self.fs(11), "bold"),
                 bg=bg, fg=c["success"] if gpa_str != "—" else c["fg_soft"],
                 width=10, pady=10).pack(side="left")
        tk.Label(row, text=rank, font=(FONT_FAMILY, self.fs(10), "bold"),
                 bg=bg, fg=c["accent_dark"], width=12, pady=10,
                 wraplength=100).pack(side="left")
        act = tk.Frame(row, bg=bg, width=14); act.pack(side="left", padx=5)
        tk.Button(act, text="✏️", font=(FONT_FAMILY, 12, "bold"),
                  bg=c["success"], fg="white", bd=0, padx=10, pady=4,
                  cursor="hand2", command=lambda idx=self.students.index(s): self.edit_student_name(idx)
                  ).pack(side="left", padx=3)
        tk.Button(act, text="✖", font=(FONT_FAMILY, 12, "bold"),
                  bg=c["danger"], fg="white", bd=0, padx=10, pady=4,
                  cursor="hand2", command=lambda idx=self.students.index(s): self.delete_student(idx)
                  ).pack(side="left", padx=3)
        def open_score(e, stu=s):
            self.current_student = stu
            self.show_score_entry(); self.fade_in_content()
        name_lbl.bind("<Button-1>", open_score)

    def add_student(self):
        name = self.ent_name.get().strip()
        if not name:
            messagebox.showwarning("⚠️", self.t("empty_warning")); return
        name = capitalize_name(name)
        if any(s["name"].lower() == name.lower() for s in self.students):
            messagebox.showerror("❌", self.t("dup_warning")); return
        self.students.append({"name": name, "scores": {}})
        self.ent_name.delete(0, tk.END)
        self.refresh_student_list(); self.beep("success")
        self.save_data(silent=True)

    def edit_student_name(self, idx):
        s = self.students[idx]
        new_name = simpledialog.askstring(self.t("edit_student"),
                                          f"{self.t('new_name')}:", initialvalue=s["name"])
        if not new_name or not new_name.strip(): return
        new_name = capitalize_name(new_name.strip())
        if any(i != idx and st["name"].lower() == new_name.lower()
               for i, st in enumerate(self.students)):
            messagebox.showerror("❌", self.t("dup_warning")); return
        s["name"] = new_name
        self.refresh_student_list(); self.beep("success"); self.save_data(silent=True)

    def delete_student(self, idx):
        if not messagebox.askyesno("⚠️", self.t("delete_student_confirm")): return
        del self.students[idx]
        self.refresh_student_list(); self.beep("success"); self.save_data(silent=True)

    def calc_gpa(self, student):
        scores = student.get("scores", {})
        tc_sum, pt_sum = 0, 0
        for subj, sc in scores.items():
            if sc.get("tb","") == "": continue
            tc = DANH_SACH_MON_PHANG.get(subj, 0)
            try: tb = float(sc["tb"])
            except (ValueError, TypeError): continue
            tc_sum += tc; pt_sum += tb*tc
        if tc_sum == 0: return 0.0, "—"
        gpa = pt_sum / tc_sum
        return gpa, self.rank_text(gpa)

    def rank_text(self, gpa):
        if self.lang == "vi":
            if gpa >= 3.6: return "Xuất sắc"
            elif gpa >= 3.2: return "Giỏi"
            elif gpa >= 2.5: return "Khá"
            elif gpa >= 2.0: return "Trung bình"
            elif gpa >= 1.0: return "Kém"
            else: return "Yếu"
        else:
            if gpa >= 3.6: return "Excellent"
            elif gpa >= 3.2: return "Very Good"
            elif gpa >= 2.5: return "Good"
            elif gpa >= 2.0: return "Average"
            elif gpa >= 1.0: return "Weak"
            else: return "Poor"

    # ============ BẢNG ĐIỂM ============
    def show_score_entry(self):
        self.clear_content()
        s = self.current_student
        if s is None: return
        c = THEMES[self.theme]
        head = tk.Frame(self.content, bg=c["bg"], pady=15); head.pack(fill="x", padx=40)
        tk.Button(head, text="⬅  " + self.t("back"),
                  font=(FONT_FAMILY, self.fs(10), "bold"),
                  bg=c["primary"], fg="white", bd=0, padx=15, pady=8, cursor="hand2",
                  command=lambda: (self.navigate("students", self.show_students),
                                   self.fade_in_content())).pack(side="left")
        tk.Label(head, text=f"📊  {self.t('score_entry')}: {s['name']}",
                 font=(FONT_FAMILY, self.fs(22), "bold"),
                 bg=c["bg"], fg=c["primary"]).pack(side="left", padx=20)
        self.lbl_gpa_rt = tk.Label(head, text="", font=(FONT_FAMILY, self.fs(13), "bold"),
                                    bg=c["bg"], fg=c["success"])
        self.lbl_gpa_rt.pack(side="right"); self.update_gpa_realtime()

        sb = tk.Frame(self.content, bg=c["card_bg"],
                      highlightbackground=c["grid"], highlightthickness=1)
        sb.pack(fill="x", padx=40, pady=(5,10), ipady=10)
        si = tk.Frame(sb, bg=c["card_bg"]); si.pack(fill="x", padx=15)
        tk.Label(si, text="🔍", font=(FONT_FAMILY, 12),
                 bg=c["card_bg"], fg=c["fg"]).pack(side="left", padx=(0,8))
        self.ent_search_subj = ttk.Entry(si, width=40, font=(FONT_FAMILY, self.fs(11)))
        self.ent_search_subj.pack(side="left", ipady=5)
        self._subj_after = None
        self.ent_search_subj.bind("<KeyRelease>", self._on_subj_debounce)
        tk.Label(si, text=f"💡 {self.t('score_hint')}", font=(FONT_FAMILY, self.fs(10)),
                 bg=c["card_bg"], fg=c["fg_soft"]).pack(side="left", padx=15)

        self.score_scroll = ScrollableFrame(self.content, bg=c["bg"])
        self.score_scroll.pack(fill="both", expand=True, padx=40, pady=(0,15))
        self._score_labels = {}
        self.render_score_table()

    def _on_subj_debounce(self, e=None):
        if self._subj_after: self.root.after_cancel(self._subj_after)
        self._subj_after = self.root.after(300, self.render_score_table)

    def render_score_table(self):
        c = THEMES[self.theme]
        parent = self.score_scroll.scrollable_frame
        for w in parent.winfo_children(): w.destroy()
        self._score_labels = {}
        s = self.current_student
        if s is None: return
        kw = self.ent_search_subj.get().strip().lower() if hasattr(self, "ent_search_subj") else ""

        hdr = tk.Frame(parent, bg=c["primary"]); hdr.pack(fill="x", pady=(0,1))
        tk.Label(hdr, text=self.t("subject"), font=(FONT_FAMILY, self.fs(10), "bold"),
                 bg=c["primary"], fg="white", anchor="w", padx=10, pady=10
                 ).pack(side="left", fill="x", expand=True)
        for txt, w in [(self.t("credits"),6),(self.t("process"),13),(self.t("midterm"),13),
                       (self.t("final"),13),(self.t("avg"),13),(self.t("rank"),15)]:
            tk.Label(hdr, text=txt, font=(FONT_FAMILY, self.fs(10), "bold"),
                     bg=c["primary"], fg="white", width=w, pady=10).pack(side="left", padx=1)

        for hk, subjects in CHUONG_TRINH_DAO_TAO.items():
            filt = [(t, tc) for t, tc in subjects if (not kw or kw in t.lower())]
            if not filt: continue
            hr = tk.Frame(parent, bg=c["primary_light"]); hr.pack(fill="x", pady=(8,1))
            tk.Label(hr, text=f"  📖 {hk}", font=(FONT_FAMILY, self.fs(11), "bold"),
                     bg=c["primary_light"], fg="white", anchor="w", pady=8).pack(fill="x")
            for ten, tc in filt:
                self.render_subject_row(parent, ten, tc)

    def render_subject_row(self, parent, ten_mon, tc):
        c = THEMES[self.theme]
        s = self.current_student
        sc = s["scores"].get(ten_mon, {"qt":"", "gk":"", "ck":"", "tb":""})
        row = tk.Frame(parent, bg=c["card_bg"],
                       highlightbackground=c["grid"], highlightthickness=1)
        row.pack(fill="x", pady=1)
        tk.Label(row, text=ten_mon, font=(FONT_FAMILY, self.fs(11)),
                 bg=c["card_bg"], fg=c["fg"], anchor="w",
                 padx=10, pady=8, wraplength=400, justify="left"
                 ).pack(side="left", fill="x", expand=True)
        tk.Label(row, text=f"{tc:g}", font=(FONT_FAMILY, self.fs(10), "bold"),
                 bg=c["bg_alt"], fg=c["primary"], width=6, pady=8).pack(side="left", padx=1)
        entries = {}
        for key in ("qt","gk","ck"):
            ent = tk.Entry(row, width=10, font=(FONT_FAMILY, self.fs(11)),
                           justify="center", bd=1, relief="solid",
                           highlightthickness=1, highlightbackground=c["grid"])
            ent.insert(0, str(sc.get(key, "")))
            ent.pack(side="left", padx=1, pady=6, ipady=3)
            entries[key] = ent
            ent.bind("<FocusOut>", lambda e, m=ten_mon, t=tc, en=entries: self.compute_score(m, t, en))
            ent.bind("<Return>", lambda e, m=ten_mon, t=tc, en=entries: self.compute_score(m, t, en))
        tb_val = sc.get("tb", "")
        lbl_tb = tk.Label(row, text=str(tb_val) if tb_val != "" else "—",
                          font=(FONT_FAMILY, self.fs(11), "bold"),
                          bg=c["card_bg"], fg=c["fg"], width=13, pady=8)
        lbl_tb.pack(side="left", padx=1)
        lbl_rank = tk.Label(row, text="", font=(FONT_FAMILY, self.fs(10), "bold"),
                            bg=c["card_bg"], fg=c["fg"], width=15, pady=8,
                            wraplength=110, justify="center")
        lbl_rank.pack(side="left", padx=1)
        if tb_val != "":
            try: self.paint_score(float(tb_val), lbl_tb, lbl_rank)
            except (ValueError, TypeError): pass
        self._score_labels[ten_mon] = (lbl_tb, lbl_rank)

    def compute_score(self, ten_mon, tc, entries):
        s = self.current_student
        if s is None: return
        try:
            qt_s = entries["qt"].get().strip(); gk_s = entries["gk"].get().strip()
            ck_s = entries["ck"].get().strip()
            if not qt_s and not gk_s and not ck_s:
                s["scores"].pop(ten_mon, None)
                if ten_mon in self._score_labels:
                    lt, lr = self._score_labels[ten_mon]
                    lt.config(text="—", bg=self.c("card_bg"), fg=self.c("fg"))
                    lr.config(text="", bg=self.c("card_bg"))
                self.update_gpa_realtime(); self.save_data(silent=True); return
            if not (qt_s and gk_s and ck_s):
                if ten_mon in self._score_labels:
                    lt, lr = self._score_labels[ten_mon]
                    lt.config(text="⏳", bg=self.c("card_bg"), fg=self.c("warning"))
                    lr.config(text=self.t("score_hint"), bg=self.c("card_bg"), fg=self.c("warning"))
                return
            qt, gk, ck = float(qt_s), float(gk_s), float(ck_s)
            for d in (qt, gk, ck):
                if d < 0 or d > 10:
                    messagebox.showerror("❌", self.t("score_range_warning")); return
            tb10 = qt*0.20 + gk*0.20 + ck*0.60
            tb4 = round(tb10/2.5, 2)
            if tb4 > 4.0: tb4 = 4.0
            s["scores"][ten_mon] = {"qt": qt_s, "gk": gk_s, "ck": ck_s, "tb": tb4}
            if ten_mon in self._score_labels:
                lt, lr = self._score_labels[ten_mon]
                lt.config(text=str(tb4)); self.paint_score(tb4, lt, lr)
            self.update_gpa_realtime()
            if self.settings["notify_on"]: self.show_toast(tb4)
            self.save_data(silent=True)
        except ValueError:
            messagebox.showerror("❌", "Vui lòng chỉ nhập số!")

    def paint_score(self, tb4, lt, lr):
        if tb4 >= 3.6: bg, fg, rank = "#15803D", "white", ("Xuất sắc" if self.lang=="vi" else "Excellent")
        elif tb4 >= 3.2: bg, fg, rank = "#16A34A", "white", ("Giỏi" if self.lang=="vi" else "Very Good")
        elif tb4 >= 2.5: bg, fg, rank = "#F59E0B", "black", ("Khá" if self.lang=="vi" else "Good")
        elif tb4 >= 2.0: bg, fg, rank = "#EA580C", "white", ("Trung bình" if self.lang=="vi" else "Average")
        elif tb4 >= 1.0: bg, fg, rank = "#DC2626", "white", ("Kém" if self.lang=="vi" else "Weak")
        else: bg, fg, rank = "#7F1D1D", "white", ("Yếu" if self.lang=="vi" else "Poor")
        lt.config(bg=bg, fg=fg); lr.config(bg=bg, fg=fg, text=rank)

    def update_gpa_realtime(self):
        if not hasattr(self, "lbl_gpa_rt"): return
        if self.current_student is None: return
        gpa, rank = self.calc_gpa(self.current_student)
        if gpa > 0:
            txt = f"🎯 GPA: {gpa:.2f}  |  {self.t('rank')}: {rank}"
            col = self.c("success") if gpa >= 2.5 else self.c("danger")
        else: txt, col = "🎯 GPA: —", self.c("fg_soft")
        self.lbl_gpa_rt.config(text=txt, fg=col)

    def show_toast(self, tb4):
        t = tk.Toplevel(self.root); t.overrideredirect(True)
        if tb4 >= 3.6: bg, ic, ms, snd = "#15803D", "🌟", "Xuất sắc! Tuyệt vời!", "excellent"
        elif tb4 >= 3.2: bg, ic, ms, snd = "#16A34A", "😊", "Giỏi lắm! Cố gắng phát huy!", "good"
        elif tb4 >= 2.5: bg, ic, ms, snd = "#F59E0B", "🙂", "Khá tốt! Cần cố gắng thêm.", "ok"
        elif tb4 >= 2.0: bg, ic, ms, snd = "#EA580C", "😐", "Trung bình. Chăm chỉ hơn nhé!", "meh"
        elif tb4 >= 1.0: bg, ic, ms, snd = "#DC2626", "😟", "Kém quá! Cần cải thiện!", "bad"
        else: bg, ic, ms, snd = "#7F1D1D", "😭", "Yếu! Nguy cơ nợ môn cao!", "bad"
        t.configure(bg=bg)
        w, h = 420, 100
        sw, sh = t.winfo_screenwidth(), t.winfo_screenheight()
        t.geometry(f"{w}x{h}+{sw-w-30}+{sh-h-80}")
        tk.Label(t, text=ic, font=("Segoe UI", 32), bg=bg, fg="white").pack(side="left", padx=15)
        tk.Label(t, text=ms, font=(FONT_FAMILY, self.fs(12), "bold"),
                 bg=bg, fg="white", wraplength=300, justify="left").pack(side="left", padx=5)
        self.beep(snd); t.after(2000, t.destroy)

    # ============ CHƯƠNG TRÌNH ============
    def show_program(self):
        self.clear_content()
        c = THEMES[self.theme]
        head = tk.Frame(self.content, bg=c["bg"], pady=15); head.pack(fill="x", padx=40)
        tk.Label(head, text="📚  " + self.t("program"),
                 font=(FONT_FAMILY, self.fs(24), "bold"),
                 bg=c["bg"], fg=c["primary"]).pack(anchor="w")
        tk.Label(head, text=f"{self.t('university')} - {self.t('program_name')}",
                 font=(FONT_FAMILY, self.fs(10)), bg=c["bg"], fg=c["fg_soft"]).pack(anchor="w")
        scroll = ScrollableFrame(self.content, bg=c["bg"])
        scroll.pack(fill="both", expand=True, padx=40, pady=10)
        parent = scroll.scrollable_frame
        grid = tk.Frame(parent, bg=c["bg"]); grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=1, uniform="col")
        grid.grid_columnconfigure(1, weight=1, uniform="col")
        total = 0
        for i, (hk, subjects) in enumerate(CHUONG_TRINH_DAO_TAO.items()):
            r, col = i//2, i%2
            hk_card = tk.Frame(grid, bg=c["card_bg"],
                               highlightbackground=c["grid"], highlightthickness=2)
            hk_card.grid(row=r, column=col, padx=8, pady=8, sticky="nsew")
            hh = tk.Frame(hk_card, bg=c["primary"]); hh.pack(fill="x")
            tk.Label(hh, text=f"  📖  {hk}", font=(FONT_FAMILY, self.fs(12), "bold"),
                     bg=c["primary"], fg="white", anchor="w", pady=10).pack(fill="x")
            body = tk.Frame(hk_card, bg=c["card_bg"]); body.pack(fill="x", padx=15, pady=10)
            hk_t = 0
            for j, (ten, tc) in enumerate(subjects, 1):
                rr = tk.Frame(body, bg=c["card_bg"]); rr.pack(fill="x", pady=2)
                tk.Label(rr, text=f"{j}.", font=(FONT_FAMILY, self.fs(10)),
                         bg=c["card_bg"], fg=c["fg_soft"], width=3, anchor="w").pack(side="left")
                tk.Label(rr, text=ten, font=(FONT_FAMILY, self.fs(11)),
                         bg=c["card_bg"], fg=c["fg"], anchor="w",
                         wraplength=380, justify="left").pack(side="left", fill="x", expand=True)
                tk.Label(rr, text=f"{tc:g} TC", font=(FONT_FAMILY, self.fs(10), "bold"),
                         bg=c["card_bg"], fg=c["primary"], padx=5).pack(side="right")
                hk_t += tc
            tk.Frame(body, bg=c["grid"], height=1).pack(fill="x", pady=(8,4))
            tk.Label(body, text=f"Tổng: {hk_t:g} tín chỉ",
                     font=(FONT_FAMILY, self.fs(10), "bold"),
                     bg=c["card_bg"], fg=c["primary"], anchor="e").pack(anchor="e")
            total += hk_t
        sb = tk.Frame(parent, bg=c["primary"], pady=15); sb.pack(fill="x", pady=15)
        tk.Label(sb, text=f"🎓 TỔNG TÍN CHỈ TOÀN KHÓA: {total:g}",
                 font=(FONT_FAMILY, self.fs(14), "bold"),
                 bg=c["primary"], fg=c["accent"]).pack()

    # ============ CÀI ĐẶT ============
    def show_settings(self):
        self.clear_content()
        c = THEMES[self.theme]
        head = tk.Frame(self.content, bg=c["bg"], pady=15); head.pack(fill="x", padx=40)
        tk.Label(head, text="⚙️  " + self.t("settings"),
                 font=(FONT_FAMILY, self.fs(24), "bold"),
                 bg=c["bg"], fg=c["primary"]).pack(anchor="w")
        scroll = ScrollableFrame(self.content, bg=c["bg"])
        scroll.pack(fill="both", expand=True, padx=40, pady=10)
        parent = scroll.scrollable_frame

        b1 = self._card(parent, "🌐", self.t("language"), "Chọn ngôn ngữ / Choose language")
        tk.Button(b1, text=f"🇻🇳 {self.t('language_vi')}", font=(FONT_FAMILY, self.fs(10), "bold"),
                  bg=c["primary"], fg="white", bd=0, padx=20, pady=8, cursor="hand2",
                  command=lambda: self.change_language("vi")).pack(side="left", padx=10)
        tk.Button(b1, text=f"🇬🇧 {self.t('language_en')}", font=(FONT_FAMILY, self.fs(10), "bold"),
                  bg=c["danger"], fg="white", bd=0, padx=20, pady=8, cursor="hand2",
                  command=lambda: self.change_language("en")).pack(side="left", padx=10)

        b2 = self._card(parent, "🎨", self.t("theme"), "Chế độ sáng/tối")
        tk.Button(b2, text=f"☀️ {self.t('light')}", font=(FONT_FAMILY, self.fs(10), "bold"),
                  bg=c["accent"], fg="black", bd=0, padx=20, pady=8, cursor="hand2",
                  command=lambda: self.change_theme("light")).pack(side="left", padx=10)
        tk.Button(b2, text=f"🌙 {self.t('dark')}", font=(FONT_FAMILY, self.fs(10), "bold"),
                  bg=BK_NAVY, fg="white", bd=0, padx=20, pady=8, cursor="hand2",
                  command=lambda: self.change_theme("dark")).pack(side="left", padx=10)

        b3 = self._card(parent, "🔤", self.t("font_size"), "Điều chỉnh cỡ chữ")
        for lbl, sc in [("Nhỏ",0.85),("Vừa",1.0),("Lớn",1.15),("Rất lớn",1.3)]:
            active = (self.settings["font_scale"] == sc)
            tk.Button(b3, text=lbl, font=(FONT_FAMILY, self.fs(10), "bold"),
                      bg=c["primary"] if active else c["border"],
                      fg="white" if active else c["fg"],
                      bd=0, padx=15, pady=8, cursor="hand2",
                      command=lambda s=sc: self.change_font_scale(s)).pack(side="left", padx=5)

        b4 = self._card(parent, "🔊", self.t("notifications"), "Bật/tắt âm thanh & thông báo")
        self._toggle(b4, self.t("sound"), self.settings["sound_on"],
                     lambda: self.toggle_setting("sound_on"))
        self._toggle(b4, self.t("notify"), self.settings["notify_on"],
                     lambda: self.toggle_setting("notify_on"))

        b5 = self._card(parent, "💾", self.t("data_management"), "Nhập/Xuất dữ liệu (tự động lưu)")
        tk.Button(b5, text=f"📂 {self.t('import')}", font=(FONT_FAMILY, self.fs(10), "bold"),
                  bg=c["primary_light"], fg="white", bd=0, padx=20, pady=8, cursor="hand2",
                  command=self.import_data).pack(side="left", padx=5)
        tk.Button(b5, text=f"📤 {self.t('export')}", font=(FONT_FAMILY, self.fs(10), "bold"),
                  bg=c["accent"], fg="black", bd=0, padx=20, pady=8, cursor="hand2",
                  command=self.export_data).pack(side="left", padx=5)

    def _card(self, parent, icon, title, desc):
        c = THEMES[self.theme]
        card = tk.Frame(parent, bg=c["card_bg"],
                        highlightbackground=c["grid"], highlightthickness=1)
        card.pack(fill="x", pady=10)
        head = tk.Frame(card, bg=c["card_bg"]); head.pack(fill="x", padx=20, pady=(15,5))
        tk.Label(head, text=icon, font=("Segoe UI", 22),
                 bg=c["card_bg"], fg=c["primary"]).pack(side="left", padx=(0,10))
        tb = tk.Frame(head, bg=c["card_bg"]); tb.pack(side="left")
        tk.Label(tb, text=title, font=(FONT_FAMILY, self.fs(14), "bold"),
                 bg=c["card_bg"], fg=c["primary"], anchor="w").pack(anchor="w")
        tk.Label(tb, text=desc, font=(FONT_FAMILY, self.fs(10)),
                 bg=c["card_bg"], fg=c["fg_soft"], anchor="w").pack(anchor="w")
        body = tk.Frame(card, bg=c["card_bg"]); body.pack(fill="x", padx=20, pady=10)
        return body

    def _toggle(self, parent, label, is_on, cmd):
        c = THEMES[self.theme]
        text = f"{label}: {'🟢 '+self.t('on') if is_on else '🔴 '+self.t('off')}"
        tk.Button(parent, text=text, font=(FONT_FAMILY, self.fs(10), "bold"),
                  bg=c["success"] if is_on else c["danger"], fg="white",
                  bd=0, padx=15, pady=8, cursor="hand2",
                  command=cmd).pack(side="left", padx=5)

    def toggle_setting(self, k):
        self.settings[k] = not self.settings[k]
        self.save_data(silent=True); self.show_settings()

    def change_font_scale(self, sc):
        self.settings["font_scale"] = sc
        self.save_data(silent=True); self.apply_theme()
        cur = self.current_page; self.build_main_ui()
        self.navigate(cur, {"home":self.show_home,"students":self.show_students,
                            "program":self.show_program,"settings":self.show_settings,
                            "about":self.show_about}.get(cur, self.show_home))
        self.fade_in_content()

    # ============ GIỚI THIỆU ============
    def show_about(self):
        self.clear_content()
        c = THEMES[self.theme]
        scroll = ScrollableFrame(self.content, bg=c["bg"])
        scroll.pack(fill="both", expand=True, padx=40, pady=15)
        parent = scroll.scrollable_frame
        tk.Label(parent, text="ℹ️  " + self.t("about_title"),
                 font=(FONT_FAMILY, self.fs(24), "bold"),
                 bg=c["bg"], fg=c["primary"]).pack(anchor="w", pady=(0,15))

        info = tk.Frame(parent, bg=c["card_bg"],
                        highlightbackground=c["grid"], highlightthickness=1)
        info.pack(fill="x", pady=10, ipady=20)
        lc = tk.Canvas(info, width=130, height=130, bg=c["card_bg"], highlightthickness=0)
        lc.pack(pady=(10,5)); draw_app_logo(lc, 130)
        tk.Label(info, text="GRADEX ELITE", font=(FONT_FAMILY, self.fs(24), "bold"),
                 bg=c["card_bg"], fg=c["primary"]).pack(pady=(5,2))
        tk.Label(info, text=self.t("app_sub"), font=(FONT_FAMILY, self.fs(12), "italic"),
                 bg=c["card_bg"], fg=c["fg_soft"]).pack()
        tk.Label(info, text=self.t("university"), font=(FONT_FAMILY, self.fs(11)),
                 bg=c["card_bg"], fg=c["fg"]).pack(pady=(8,3))
        tk.Label(info, text=f"{self.t('faculty')} - {self.t('program_name')}",
                 font=(FONT_FAMILY, self.fs(11)), bg=c["card_bg"], fg=c["fg"]).pack()
        tk.Label(info, text=f"{self.t('build_date')}: {BUILD_DATE}",
                 font=(FONT_FAMILY, self.fs(10), "italic"),
                 bg=c["card_bg"], fg=c["fg_soft"]).pack(pady=(8,0))

        desc_box = tk.Frame(info, bg=c["bg_alt"], padx=20, pady=15)
        desc_box.pack(fill="x", padx=40, pady=(15,5))
        tk.Label(desc_box, text="📝 Mô tả phần mềm",
                 font=(FONT_FAMILY, self.fs(12), "bold"),
                 bg=c["bg_alt"], fg=c["primary"], anchor="w").pack(anchor="w", pady=(0,5))
        tk.Label(desc_box, text=self.t("app_desc"),
                 font=(FONT_FAMILY, self.fs(11)),
                 bg=c["bg_alt"], fg=c["fg"], wraplength=900,
                 justify="left", anchor="w").pack(anchor="w")

        tb = tk.Frame(parent, bg=c["card_bg"],
                      highlightbackground=c["grid"], highlightthickness=1)
        tb.pack(fill="x", pady=10, ipady=15)
        tk.Label(tb, text="👥  " + self.t("team"), font=(FONT_FAMILY, self.fs(18), "bold"),
                 bg=c["card_bg"], fg=c["primary"]).pack(anchor="w", padx=20, pady=(10,10))
        for name, role in [
            ("Đỗ Thanh Phong", self.t("leader") + " - Điều hành & Kiểm thử"),
            ("Trần Trung Đỉnh", self.t("member") + " - Lập trình chính"),
            ("Nguyễn Phước Đạt", self.t("member") + " - Thiết kế giao diện"),
            ("Trần Minh Trí", self.t("member") + " - Xử lý logic")]:
            r = tk.Frame(tb, bg=c["card_bg"]); r.pack(fill="x", padx=20, pady=3)
            tk.Label(r, text="👤", font=("Segoe UI", 14),
                     bg=c["card_bg"], fg=c["accent_dark"]).pack(side="left", padx=(0,10))
            tk.Label(r, text=name, font=(FONT_FAMILY, self.fs(11), "bold"),
                     bg=c["card_bg"], fg=c["fg"], width=22, anchor="w").pack(side="left")
            tk.Label(r, text=role, font=(FONT_FAMILY, self.fs(11)),
                     bg=c["card_bg"], fg=c["fg_soft"], anchor="w").pack(side="left")
        tk.Label(tb, text=f"👨‍🏫 {self.t('instructor')}: Nguyễn Thanh Hải",
                 font=(FONT_FAMILY, self.fs(12), "bold"),
                 bg=c["card_bg"], fg=c["danger"]).pack(pady=(15,5))

        fb = tk.Frame(parent, bg=c["card_bg"],
                      highlightbackground=c["grid"], highlightthickness=1)
        fb.pack(fill="x", pady=10, ipady=15)
        tk.Label(fb, text="✨  " + self.t("features"),
                 font=(FONT_FAMILY, self.fs(18), "bold"),
                 bg=c["card_bg"], fg=c["primary"]).pack(anchor="w", padx=20, pady=(10,10))
        for f in ["Quản lý danh sách sinh viên theo lớp",
                  "Nhập điểm tự động 20% - 20% - 60%",
                  "Quy đổi thang điểm 4 và xếp loại học lực",
                  "Tìm kiếm học phần và sinh viên",
                  "Sửa/xóa tên sinh viên, tự động viết hoa",
                  "Âm thanh và cảm xúc theo mức điểm",
                  "Giao diện Sáng/Tối hiện đại, chữ to rõ",
                  "Song ngữ Anh - Việt, tự động lưu dữ liệu"]:
            tk.Label(fb, text=f"  ✅  {f}", font=(FONT_FAMILY, self.fs(11)),
                     bg=c["card_bg"], fg=c["fg"], anchor="w").pack(fill="x", padx=25, pady=2)
        tk.Label(parent, text=f'"{self.t("slogan")}"',
                 font=(FONT_FAMILY, self.fs(14), "italic"),
                 bg=c["bg"], fg=c["primary"]).pack(pady=20)

    # ============ ĐỔI NGÔN NGỮ/THEME ============
    def change_language(self, lang):
        self.lang = lang; self.save_data(silent=True)
        self.apply_theme(); self.build_main_ui()
        self.navigate("settings", self.show_settings); self.fade_in_content()

    def toggle_language(self):
        self.lang = "en" if self.lang == "vi" else "vi"
        self.save_data(silent=True); self.apply_theme()
        cur = self.current_page; self.build_main_ui()
        self.navigate(cur, {"home":self.show_home,"students":self.show_students,
                            "program":self.show_program,"settings":self.show_settings,
                            "about":self.show_about}.get(cur, self.show_home))
        self.fade_in_content()

    def change_theme(self, theme):
        self.theme = theme; self.save_data(silent=True)
        self.apply_theme(); self.build_main_ui()
        self.navigate("settings", self.show_settings); self.fade_in_content()

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.save_data(silent=True); self.apply_theme()
        cur = self.current_page; self.build_main_ui()
        self.navigate(cur, {"home":self.show_home,"students":self.show_students,
                            "program":self.show_program,"settings":self.show_settings,
                            "about":self.show_about}.get(cur, self.show_home))
        self.fade_in_content()

    # ============ LƯU/TẢI ============
    def save_data(self, silent=False):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump({"students": self.students, "theme": self.theme,
                           "lang": self.lang, "settings": self.settings},
                          f, ensure_ascii=False, indent=2)
        except Exception as e:
            if not silent: messagebox.showerror("❌", f"Lỗi lưu: {e}")

    def load_data(self):
        if not os.path.exists(self.data_file): return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f: data = json.load(f)
            self.students = data.get("students", [])
            if "settings" in data: self.settings.update(data["settings"])
        except Exception: self.students = []

    def import_data(self):
        path = filedialog.askopenfilename(title="Chọn file dữ liệu",
            filetypes=[("JSON files","*.json"),("All files","*.*")])
        if not path: return
        try:
            with open(path, "r", encoding="utf-8") as f: data = json.load(f)
            self.students = data.get("students", [])
            self.refresh_student_list()
            self.beep("success"); messagebox.showinfo("✅", self.t("loaded"))
            self.save_data(silent=True)
        except Exception as e: messagebox.showerror("❌", f"Lỗi: {e}")

    def export_data(self):
        path = filedialog.asksaveasfilename(title="Xuất dữ liệu",
            defaultextension=".json", filetypes=[("JSON files","*.json")])
        if not path: return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"students": self.students}, f, ensure_ascii=False, indent=2)
            self.beep("success"); messagebox.showinfo("✅", f"Đã xuất: {path}")
        except Exception as e: messagebox.showerror("❌", f"Lỗi: {e}")

    def on_close(self):
        self.save_data(silent=True); self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeXEliteApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()