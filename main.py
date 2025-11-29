import tkinter as tk
from tkinter import messagebox
import subprocess
import ctypes
import sys

class AdobeGenuineServiceStopperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adobe Genuine 停止ツール")
        self.root.geometry("650x700")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(False, False)
        
        self.service_name = "Adobe Genuine Software Integrity Service"
        
        # 管理者権限チェック
        # -------------------------------------------------------
        if not self.is_admin():
            self.restart_as_admin()
            return
        
        # ヘッダーセクション
        # -------------------------------------------------------
        header_frame = tk.Frame(root, bg="#ffffff", relief="flat")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="Adobe Genuine 停止ツール",
            font=("Yu Gothic UI", 20, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="サービスを停止し、自動実行を無効化します",
            font=("Yu Gothic UI", 10),
            bg="#ffffff",
            fg="#666666"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # ステータス表示セクション
        # -------------------------------------------------------
        status_frame = tk.Frame(root, bg="#ffffff", relief="flat")
        status_frame.pack(fill="x", padx=20, pady=10)
        
        status_label_title = tk.Label(
            status_frame,
            text="サービス状態",
            font=("Yu Gothic UI", 11, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        status_label_title.pack(pady=(15, 10))
        
        self.status_label = tk.Label(
            status_frame,
            text="● 確認していません",
            font=("Yu Gothic UI", 12),
            fg="#666666",
            bg="#ffffff"
        )
        self.status_label.pack(pady=(0, 15))
        
        # アクションボタンセクション
        # -------------------------------------------------------
        button_frame = tk.Frame(root, bg="#f5f5f5")
        button_frame.pack(pady=15)
        
        self.check_button = tk.Button(
            button_frame,
            text="稼働状況を更新",
            command=self.check_service,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Yu Gothic UI", 11, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.check_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = tk.Button(
            button_frame,
            text="サービスを停止",
            command=self.stop_and_disable_service,
            width=20,
            height=2,
            bg="#f44336",
            fg="white",
            font=("Yu Gothic UI", 11, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # 実行ログセクション
        # -------------------------------------------------------
        log_frame = tk.Frame(root, bg="#ffffff", relief="flat")
        log_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        log_title = tk.Label(
            log_frame,
            text="実行ログ",
            font=("Yu Gothic UI", 11, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        log_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # テキストエリアとスクロールバー
        text_container = tk.Frame(log_frame, bg="#ffffff")
        text_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side="right", fill="y")
        
        self.result_text = tk.Text(
            text_container,
            font=("Consolas", 11),
            bg="#fafafa",
            fg="#333333",
            relief="solid",
            bd=1,
            padx=10,
            pady=10,
            yscrollcommand=scrollbar.set,
            wrap="word"
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        # 隠しメニュー用のキーバインド
        # -------------------------------------------------------
        # self.root.bind('<Control-d>', lambda e: self.open_hidden_menu())
        self.root.bind('<Control-D>', lambda e: self.open_hidden_menu())
        
        # 初回チェック
        # -------------------------------------------------------
        self.root.after(500, self.check_service)
    
    
    # 管理者権限チェック機能
    # -------------------------------------------------------
    def is_admin(self):
        """管理者権限で実行されているか確認"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def restart_as_admin(self):
        """管理者権限で再起動"""
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except:
            messagebox.showerror(
                "エラー",
                "管理者権限で実行できませんでした。\n手動で「管理者として実行」してください。"
            )
        sys.exit()
    
    # ログ管理機能
    # -------------------------------------------------------
    def log_message(self, message):
        """結果エリアにメッセージを追加"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """結果エリアをクリア"""
        self.result_text.delete(1.0, tk.END)
    
    # サービス確認機能
    # -------------------------------------------------------
    def check_service(self):
        """Adobe Genuineの存在と状態を確認"""
        self.clear_log()
        self.log_message("=" * 60)
        self.log_message("Adobe Genuine 確認中...")
        self.log_message("=" * 60)
        
        try:
            # sc query コマンドでサービス確認
            result = subprocess.run(
                ["sc", "query", self.service_name],
                capture_output=True,
                text=True,
                encoding="shift-jis",
                errors="ignore"
            )
            
            if result.returncode != 0:
                self.status_label.config(text="● サービスが見つかりません", fg="#FF5722")
                self.log_message("\n" + "!" * 60)
                self.log_message("❌ エラー: サービスが見つかりません")
                self.log_message("!" * 60)
                self.log_message(f"\n{self.service_name} は、このコンピュータに")
                self.log_message("インストールされていないか、削除されています。")
                messagebox.showerror(
                    "サービスが見つかりません", 
                    f"{self.service_name} が見つかりませんでした。\n\n"
                    "このサービスはインストールされていない可能性があります。"
                )
                return False
            # サービスの状態を解析
            output = result.stdout
            
            if "RUNNING" in output:
                status = "実行中"
                status_color = "#4CAF50"  # 緑
            elif "STOPPED" in output:
                status = "停止中"
                status_color = "#f44336"  # 赤
            else:
                status = "不明"
                status_color = "#9E9E9E"  # グレー
            
            self.status_label.config(text=f"● サービス: {status}", fg=status_color)
            self.log_message(f"\n{self.service_name} が見つかりました")
            self.log_message(f"状態: {status}")
            
            # スタートアップの種類を確認
            config_result = subprocess.run(
                ["sc", "qc", self.service_name],
                capture_output=True,
                text=True,
                encoding="shift-jis",
                errors="ignore"
            )
            
            if "AUTO_START" in config_result.stdout:
                self.log_message(f"起動設定: 自動")
            elif "DEMAND_START" in config_result.stdout:
                self.log_message(f"起動設定: 手動")
            elif "DISABLED" in config_result.stdout:
                self.log_message(f"起動設定: 無効")
            
            self.log_message("\n確認完了")
            return True
            
        except Exception as e:
            self.status_label.config(text="● 確認エラー", fg="#999999")
            self.log_message(f"\nエラー: {str(e)}")
            messagebox.showerror("エラー", f"確認に失敗しました:\n{str(e)}")
            return False
    
    # サービス停止機能
    # -------------------------------------------------------
    def stop_and_disable_service(self):
        """サービスを停止し、自動実行を無効化"""
        self.clear_log()
        self.log_message("=" * 60)
        self.log_message("Adobe Genuine 停止処理開始")
        self.log_message("=" * 60)
        
        # まずサービスの存在確認
        try:
            check_result = subprocess.run(
                ["sc", "query", self.service_name],
                capture_output=True,
                text=True,
                encoding="shift-jis",
                errors="ignore"
            )
            
            if check_result.returncode != 0:
                self.status_label.config(text="● サービスが見つかりません", fg="#999999")
                self.log_message(f"❌ {self.service_name} が見つかりませんでした")
                messagebox.showerror("エラー", f"{self.service_name} が見つかりませんでした")
                return
        
        except Exception as e:
            messagebox.showerror("エラー", f"確認に失敗しました:\n{str(e)}")
            return
        
        # 確認ダイアログ
        confirm = messagebox.askyesno(
            "確認",
            f"{self.service_name} を停止し、自動実行を無効化しますか？"
        )
        
        if not confirm:
            self.log_message("\n処理がキャンセルされました")
            return
        
        success = True
        
        # ステップ1: サービスを停止
        self.log_message("\n[ステップ 1/2] サービスを停止中...")
        try:
            stop_result = subprocess.run(
                ["net", "stop", self.service_name],
                capture_output=True,
                text=True,
                encoding="shift-jis",
                errors="ignore"
            )
            
            if stop_result.returncode == 0:
                self.log_message("サービスの停止に成功しました")
            elif "既に停止" in stop_result.stdout or "停止されています" in stop_result.stdout:
                self.log_message("サービスは既に停止されています")
            else:
                self.log_message(f"停止時に警告: {stop_result.stderr or stop_result.stdout}")
                success = False
        
        except Exception as e:
            self.log_message(f"停止エラー: {str(e)}")
            success = False
        
        # ステップ2: 自動実行を無効化
        self.log_message("\n[ステップ 2/2] 自動実行を無効化中...")
        try:
            disable_result = subprocess.run(
                ["sc", "config", self.service_name, "start=", "disabled"],
                capture_output=True,
                text=True,
                encoding="shift-jis",
                errors="ignore"
            )
            
            if disable_result.returncode == 0:
                self.log_message("自動実行の無効化に成功しました")
            else:
                self.log_message(f"無効化エラー: {disable_result.stderr or disable_result.stdout}")
                success = False
        
        except Exception as e:
            self.log_message(f"無効化エラー: {str(e)}")
            success = False
        
        # 完了メッセージ
        self.log_message("\n" + "=" * 60)
        if success:
            self.log_message("完了！")
            self.log_message("=" * 60)
            self.status_label.config(text="● 停止完了・自動実行無効化", fg="#2196F3")
            messagebox.showinfo("完了", "完了！")
        else:
            self.log_message("一部の処理が失敗しました")
            self.log_message("=" * 60)
            messagebox.showwarning("警告", "一部の処理が失敗しました。詳細を確認してください。")
        
        # 最終状態を確認
        self.root.after(1000, self.check_service)
    
    # 隠しメニュー機能
    # -------------------------------------------------------
    def open_hidden_menu(self):
        """隠しメニューを開く（Ctrl+Shift+D）"""
        hidden_window = tk.Toplevel(self.root)
        hidden_window.title("詳細設定 (Hidden Menu)")
        hidden_window.geometry("550x700")
        hidden_window.configure(bg="#f5f5f5")
        hidden_window.resizable(False, False)
        
        # ヘッダー
        header = tk.Label(
            hidden_window,
            text="🔧 詳細設定メニュー",
            font=("Yu Gothic UI", 16, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        header.pack(pady=20)
        
        # 説明
        info = tk.Label(
            hidden_window,
            text="サービスの起動設定を詳細に変更できます",
            font=("Yu Gothic UI", 9),
            bg="#f5f5f5",
            fg="#666666"
        )
        info.pack(pady=(0, 20))
        
        # コンテンツフレーム
        content_frame = tk.Frame(hidden_window, bg="#ffffff", relief="flat")
        content_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # サービス操作セクション
        operation_label = tk.Label(
            content_frame,
            text="サービス操作:",
            font=("Yu Gothic UI", 11, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        operation_label.pack(pady=(20, 10))
        
        # 操作ボタンフレーム
        operation_button_frame = tk.Frame(content_frame, bg="#ffffff")
        operation_button_frame.pack(pady=10)
        
        start_button = tk.Button(
            operation_button_frame,
            text="▶ 起動",
            command=lambda: self.control_service("start", hidden_window),
            width=12,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Yu Gothic UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        start_button.grid(row=0, column=0, padx=8, pady=5)
        
        stop_button = tk.Button(
            operation_button_frame,
            text="■ 停止",
            command=lambda: self.control_service("stop", hidden_window),
            width=12,
            height=2,
            bg="#f44336",
            fg="white",
            font=("Yu Gothic UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        stop_button.grid(row=0, column=1, padx=8, pady=5)
        
        pause_button = tk.Button(
            operation_button_frame,
            text="⏸ 一時停止",
            command=lambda: self.control_service("pause", hidden_window),
            width=12,
            height=2,
            bg="#FF9800",
            fg="white",
            font=("Yu Gothic UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        pause_button.grid(row=0, column=2, padx=8, pady=5)
        
        # 区切り線
        separator = tk.Frame(content_frame, bg="#e0e0e0", height=2)
        separator.pack(fill="x", pady=20)
        
        # 起動設定セクション
        startup_label = tk.Label(
            content_frame,
            text="起動設定を選択:",
            font=("Yu Gothic UI", 11, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        startup_label.pack(pady=(20, 10))
        
        # ラジオボタン用の変数
        startup_var = tk.StringVar(value="disabled")
        
        # ラジオボタンフレーム
        radio_frame = tk.Frame(content_frame, bg="#ffffff")
        radio_frame.pack(pady=10)
        
        options = [
            ("無効 (Disabled)", "disabled", "サービスを完全に無効化"),
            ("手動 (Manual)", "demand", "手動でのみ起動可能"),
            ("自動 (Automatic)", "auto", "システム起動時に自動起動"),
            ("自動（遅延）", "delayed-auto", "システム起動後に遅延起動")
        ]
        
        for text, value, desc in options:
            frame = tk.Frame(radio_frame, bg="#ffffff")
            frame.pack(anchor="w", pady=5)
            
            rb = tk.Radiobutton(
                frame,
                text=text,
                variable=startup_var,
                value=value,
                font=("Yu Gothic UI", 10),
                bg="#ffffff",
                fg="#333333",
                selectcolor="#ffffff"
            )
            rb.pack(side="left")
            
            desc_label = tk.Label(
                frame,
                text=f"  - {desc}",
                font=("Yu Gothic UI", 8),
                bg="#ffffff",
                fg="#999999"
            )
            desc_label.pack(side="left")
        
        # 注意事項
        warning_label = tk.Label(
            content_frame,
            text="※ 設定変更には管理者権限が必要です",
            font=("Yu Gothic UI", 8),
            bg="#ffffff",
            fg="#f44336"
        )
        warning_label.pack(pady=(10, 15))
        
        # 適用ボタン
        button_frame = tk.Frame(hidden_window, bg="#f5f5f5")
        button_frame.pack(pady=20)
        
        apply_button = tk.Button(
            button_frame,
            text="設定を適用",
            command=lambda: self.apply_startup_setting(startup_var.get(), hidden_window),
            width=15,
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Yu Gothic UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        apply_button.pack(side="left", padx=5)
        
        close_button = tk.Button(
            button_frame,
            text="閉じる",
            command=hidden_window.destroy,
            width=15,
            height=2,
            bg="#9E9E9E",
            fg="white",
            font=("Yu Gothic UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        )
        close_button.pack(side="left", padx=5)
        
        # ウィンドウを中央に配置
        hidden_window.update_idletasks()
        x = (hidden_window.winfo_screenwidth() // 2) - (hidden_window.winfo_width() // 2)
        y = (hidden_window.winfo_screenheight() // 2) - (hidden_window.winfo_height() // 2)
        hidden_window.geometry(f"+{x}+{y}")
    
    def control_service(self, action, window):
        """サービスを操作（起動・停止・一時停止）"""
        self.clear_log()
        action_names = {
            "start": "起動",
            "stop": "停止",
            "pause": "一時停止"
        }
        action_name = action_names.get(action, action)
        
        self.log_message("=" * 60)
        self.log_message(f"サービスを{action_name}中...")
        self.log_message("=" * 60)
        
        # サービスの存在確認
        try:
            check_result = subprocess.run(
                ["sc", "query", self.service_name],
                capture_output=True,
                text=True,
                encoding="shift-jis",
                errors="ignore"
            )
            
            if check_result.returncode != 0:
                self.log_message(f"\n{self.service_name} が見つかりませんでした")
                messagebox.showerror("エラー", f"{self.service_name} が見つかりませんでした")
                return
        except Exception as e:
            messagebox.showerror("エラー", f"確認に失敗しました:\n{str(e)}")
            return
        
        # サービスを操作
        try:
            if action == "start":
                result = subprocess.run(
                    ["net", "start", self.service_name],
                    capture_output=True,
                    text=True,
                    encoding="shift-jis",
                    errors="ignore"
                )
            elif action == "stop":
                result = subprocess.run(
                    ["net", "stop", self.service_name],
                    capture_output=True,
                    text=True,
                    encoding="shift-jis",
                    errors="ignore"
                )
            elif action == "pause":
                result = subprocess.run(
                    ["net", "pause", self.service_name],
                    capture_output=True,
                    text=True,
                    encoding="shift-jis",
                    errors="ignore"
                )
            
            if result.returncode == 0:
                self.log_message(f"\n{action_name}に成功しました")
                self.log_message("\n" + "=" * 60)
                self.log_message("完了！")
                self.log_message("=" * 60)
                messagebox.showinfo("完了", f"{action_name}完了！")
                # 状態を再確認
                self.root.after(500, self.check_service)
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                if "既に開始されています" in error_msg:
                    self.log_message(f"\nサービスは既に起動されています")
                    messagebox.showinfo("情報", "サービスは既に起動されています")
                elif "既に停止" in error_msg or "停止されています" in error_msg:
                    self.log_message(f"\nサービスは既に停止されています")
                    messagebox.showinfo("情報", "サービスは既に停止されています")
                else:
                    self.log_message(f"\n{action_name}エラー: {error_msg}")
                    messagebox.showerror("エラー", f"{action_name}に失敗しました:\n{error_msg}")
        
        except Exception as e:
            self.log_message(f"\nエラー: {str(e)}")
            messagebox.showerror("エラー", f"{action_name}に失敗しました:\n{str(e)}")
    
    def apply_startup_setting(self, setting, window):
        """起動設定を適用"""
        self.clear_log()
        self.log_message("=" * 60)
        self.log_message(f"起動設定を変更中: {setting}")
        self.log_message("=" * 60)
        
        # サービスの存在確認
        try:
            check_result = subprocess.run(
                ["sc", "query", self.service_name],
                capture_output=True,
                text=True,
                encoding="shift-jis",
                errors="ignore"
            )
            
            if check_result.returncode != 0:
                self.log_message(f"\n{self.service_name} が見つかりませんでした")
                messagebox.showerror("エラー", f"{self.service_name} が見つかりませんでした")
                return
        except Exception as e:
            messagebox.showerror("エラー", f"確認に失敗しました:\n{str(e)}")
            return
        
        # 設定を適用
        try:
            config_result = subprocess.run(
                ["sc", "config", self.service_name, "start=", setting],
                capture_output=True,
                text=True,
                encoding="shift-jis",
                errors="ignore"
            )
            
            if config_result.returncode == 0:
                self.log_message(f"\n起動設定の変更に成功しました")
                self.log_message(f"新しい設定: {setting}")
                self.log_message("\n" + "=" * 60)
                self.log_message("完了！")
                self.log_message("=" * 60)
                messagebox.showinfo("完了", "設定を適用しました！")
                # 状態を再確認
                self.root.after(500, self.check_service)
            else:
                self.log_message(f"\n設定変更エラー: {config_result.stderr or config_result.stdout}")
                messagebox.showerror("エラー", "設定の変更に失敗しました")
        
        except Exception as e:
            self.log_message(f"\nエラー: {str(e)}")
            messagebox.showerror("エラー", f"設定の変更に失敗しました:\n{str(e)}")


# メイン実行
# -------------------------------------------------------
def main():
    root = tk.Tk()
    app = AdobeGenuineServiceStopperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()