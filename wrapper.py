import sys
import os
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext

# 判断是否打包运行
if getattr(sys, 'frozen', False):
    # 打包后的路径
    base_path = sys._MEIPASS
    app_path = os.path.dirname(sys.executable)
else:
    # 开发环境的路径
    base_path = os.path.abspath(os.path.dirname(__file__))
    app_path = base_path

# 将基础路径添加到Python路径
if base_path not in sys.path:
    sys.path.insert(0, base_path)

# 设置工作目录为应用目录
os.chdir(app_path)

# 定义日志列表
log_messages = []

def add_log(message):
    """添加日志消息"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_messages.append(f"[{timestamp}] {message}")
    if len(log_messages) > 1000:
        log_messages.pop(0)

def run_flask_app():
    """在后台线程中运行Flask应用"""
    try:
        from app import app, db, init_models
        
        add_log("初始化模型...")
        init_models()
        
        add_log("创建数据库表...")
        with app.app_context():
            db.create_all()
        
        add_log("启动Flask服务...")
        # 运行应用，使用threaded=True支持并发
        app.run(debug=False, host='0.0.0.0', port=12456, threaded=True)
        
    except Exception as e:
        add_log(f"服务启动失败: {str(e)}")
        raise

def update_log_text(text_widget):
    """更新日志文本框"""
    def update():
        while True:
            if log_messages:
                text_widget.config(state=tk.NORMAL)
                # 只添加新的日志
                current_line_count = int(text_widget.index('end-1c').split('.')[0])
                if len(log_messages) > current_line_count:
                    for msg in log_messages[current_line_count:]:
                        text_widget.insert(tk.END, msg + "\n")
                        text_widget.see(tk.END)
                text_widget.config(state=tk.DISABLED)
            time.sleep(1)
    
    threading.Thread(target=update, daemon=True).start()

def create_gui():
    """创建GUI窗口"""
    root = tk.Tk()
    root.title("RFID管理系统服务")
    root.geometry("600x450")
    root.resizable(False, False)
    
    # 设置窗口图标（如果有）
    try:
        root.iconbitmap(default=None)
    except:
        pass
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # 状态标签
    status_frame = ttk.LabelFrame(main_frame, text="服务状态")
    status_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    # 状态指示
    status_var = tk.StringVar(value="启动中...")
    status_label = ttk.Label(status_frame, textvariable=status_var, font=('Arial', 12))
    status_label.grid(row=0, column=0, padx=10, pady=10)
    
    # 状态指示灯
    status_canvas = tk.Canvas(status_frame, width=20, height=20)
    status_canvas.grid(row=0, column=1, padx=10, pady=10)
    status_oval = status_canvas.create_oval(2, 2, 18, 18, fill="yellow")
    
    # 端口信息
    port_label = ttk.Label(status_frame, text="端口: 12456")
    port_label.grid(row=0, column=2, padx=10, pady=10)
    
    # 访问链接
    url_label = ttk.Label(status_frame, text="访问地址:", font=('Arial', 10))
    url_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    
    url_text = tk.Text(status_frame, height=2, width=50, wrap=tk.WORD)
    url_text.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
    url_text.insert(tk.END, "http://127.0.0.1:12456\nhttp://服务器IP:12456")
    url_text.config(state=tk.DISABLED)
    
    # 日志区域
    log_frame = ttk.LabelFrame(main_frame, text="运行日志")
    log_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
    
    log_text = scrolledtext.ScrolledText(log_frame, width=70, height=15, wrap=tk.WORD)
    log_text.grid(row=0, column=0, padx=5, pady=5)
    log_text.config(state=tk.DISABLED)
    
    # 启动按钮
    def start_service():
        add_log("正在启动RFID管理系统...")
        status_var.set("启动中...")
        status_canvas.itemconfig(status_oval, fill="yellow")
        
        # 在后台线程启动Flask服务
        threading.Thread(target=run_flask_app, daemon=True).start()
        
        # 检查服务是否启动成功
        def check_status():
            time.sleep(3)
            status_var.set("运行中")
            status_canvas.itemconfig(status_oval, fill="green")
            add_log("服务已成功启动！")
            add_log(f"服务运行在端口: 12456")
            add_log(f"数据库路径: {os.path.join(app_path, 'instance', 'rfid_system_new.db')}")
        
        threading.Thread(target=check_status, daemon=True).start()
    
    start_button = ttk.Button(main_frame, text="启动服务", command=start_service)
    start_button.grid(row=2, column=0, padx=5, pady=10, sticky=tk.E)
    
    # 退出按钮
    def exit_app():
        add_log("正在关闭服务...")
        root.destroy()
    
    exit_button = ttk.Button(main_frame, text="退出", command=exit_app)
    exit_button.grid(row=2, column=1, padx=5, pady=10, sticky=tk.W)
    
    # 启动日志更新
    update_log_text(log_text)
    
    # 添加初始日志
    add_log("RFID管理系统服务管理器")
    add_log("版本: 1.0")
    add_log("端口: 12456")
    add_log("点击'启动服务'开始运行")
    
    # 自动启动服务
    start_service()
    
    root.mainloop()

if __name__ == '__main__':
    create_gui()