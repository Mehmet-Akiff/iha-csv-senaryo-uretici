"""
app.py
İHA Telemetri CSV Senaryo Üretici Masaüstü Uygulaması (v1.4.0).
Bağımsız masaüstü arayüzü, otomatik sıralı/tarihli periyot klasörleme,
garantili 1.8 sn animasyonlu İHA açılış ekranı (Splash Screen), pencere fade-in
ve sekme/sayfa geçiş animasyonları.
"""

import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import pandas as pd

try:
    import pyi_splash
except ImportError:
    pyi_splash = None

from scenario_engine import TelemetryScenarioGenerator, SCENARIO_DESCRIPTIONS

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


def get_resource_path(relative_path: str) -> str:
    """PyInstaller veya taşınabilir çalışmada kaynak dosya yolunu döndürür."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class CSVGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("İHA Telemetri CSV Senaryo Üretici v1.4.0")
        self.geometry("1220x850")
        self.minsize(1000, 720)

        # İHA İkonunu Ayarla
        icon_path = get_resource_path(os.path.join("assets", "generator_icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.generator = TelemetryScenarioGenerator()
        self.current_df = None
        self.current_raw = None

        self._build_ui()

        if pyi_splash is not None:
            try:
                pyi_splash.close()
            except Exception:
                pass

        # Çok hızlı açılsa bile en az 1.8 saniye garantili animasyonlu Açılış Paneli (Splash) göster
        self._show_startup_splash()

    def _show_startup_splash(self):
        """İlk tıklamada ekranda 1.8 saniye boyunca animasyonlu İHA Senaryo Üretici yükleme paneli gösterir."""
        self.attributes("-alpha", 0.0)

        splash = tk.Toplevel(self)
        splash.overrideredirect(True)
        splash.attributes("-topmost", True)
        splash.configure(bg="#0c2018")

        w, h = 540, 310
        sw = splash.winfo_screenwidth()
        sh = splash.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        splash.geometry(f"{w}x{h}+{x}+{y}")

        border = tk.Frame(splash, bg="#2bda72", bd=0)
        border.place(x=0, y=0, width=w, height=h)
        inner = tk.Frame(border, bg="#0c2018")
        inner.place(x=2, y=2, width=w - 4, height=h - 4)

        top_bar = tk.Frame(inner, bg="#2bda72", height=5)
        top_bar.pack(fill="x", side="top")

        png_path = get_resource_path(os.path.join("assets", "generator_icon.png"))
        if os.path.exists(png_path):
            try:
                pil_img = Image.open(png_path).resize((84, 84), Image.Resampling.LANCZOS)
                self._splash_logo = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(84, 84))
                logo_lbl = ctk.CTkLabel(inner, image=self._splash_logo, text="", fg_color="#0c2018")
                logo_lbl.pack(pady=(22, 8))
            except Exception:
                pass

        title_lbl = ctk.CTkLabel(
            inner,
            text="İHA TELEMETRİ CSV SENARYO ÜRETİCİ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff",
            fg_color="#0c2018",
        )
        title_lbl.pack(pady=(2, 2))

        sub_lbl = ctk.CTkLabel(
            inner,
            text="14 Farklı Uçuş, Sensör Anomalisi ve Sınır Değer Test Simülatörü • v1.4.0",
            font=ctk.CTkFont(size=11),
            text_color="#69db7c",
            fg_color="#0c2018",
        )
        sub_lbl.pack(pady=(0, 18))

        status_lbl = ctk.CTkLabel(
            inner,
            text="İHA simülasyon profilleri yükleniyor... %0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#e9ecef",
            fg_color="#0c2018",
        )
        status_lbl.pack(pady=(0, 8))

        pbar = ctk.CTkProgressBar(inner, width=430, height=12, corner_radius=6, progress_color="#2bda72", fg_color="#16382b")
        pbar.set(0.0)
        pbar.pack(pady=(0, 14))

        footer_lbl = ctk.CTkLabel(
            inner,
            text="🛡️ DigiCert İmzalı Güvenli Çalışma Zamanı • Otomatik Tarihli/Sıralı Klasörleme",
            font=ctk.CTkFont(size=10),
            text_color="#868e96",
            fg_color="#0c2018",
        )
        footer_lbl.pack(side="bottom", pady=10)

        total_steps = 36  # ~1.8 saniye garantili açılış ekranı

        def animate_splash(step_idx=0):
            if step_idx <= total_steps:
                prog = step_idx / total_steps
                pbar.set(prog)
                pct = int(prog * 100)
                if prog < 0.30:
                    msg = f"14 farklı İHA uçuş ve hata senaryosu yükleniyor... %{pct}"
                elif prog < 0.65:
                    msg = f"Sentetik telemetri üretim motoru hazırlanıyor... %{pct}"
                elif prog < 0.90:
                    msg = f"Canlı tablo ve ham CSV önizleme katmanı başlatılıyor... %{pct}"
                else:
                    msg = f"Simülatör hazır! Arayüz açılıyor... %{pct}"
                status_lbl.configure(text=msg)
                self.after(48, animate_splash, step_idx + 1)
            else:
                try:
                    splash.destroy()
                except Exception:
                    pass
                self._fade_in_main_window()

        animate_splash(0)

    def _fade_in_main_window(self, alpha=0.0):
        """Ana pencereyi yumuşak (fade-in) animasyonla görünür yapar."""
        alpha = min(1.0, alpha + 0.12)
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(20, self._fade_in_main_window, alpha)
        else:
            self.focus_force()

    def _build_ui(self):
        top_frame = ctk.CTkFrame(self, corner_radius=10)
        top_frame.pack(fill="x", padx=15, pady=(15, 10))

        png_path = get_resource_path(os.path.join("assets", "generator_icon.png"))
        if os.path.exists(png_path):
            try:
                pil_hdr = Image.open(png_path).resize((34, 34), Image.Resampling.LANCZOS)
                self._hdr_icon = ctk.CTkImage(light_image=pil_hdr, dark_image=pil_hdr, size=(34, 34))
                hdr_img_lbl = ctk.CTkLabel(top_frame, image=self._hdr_icon, text="")
                hdr_img_lbl.pack(side="left", padx=(15, 4), pady=10)
            except Exception:
                pass

        title_lbl = ctk.CTkLabel(
            top_frame,
            text="İHA Telemetri CSV Senaryo Üretici",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_lbl.pack(side="left", padx=(6, 15), pady=12)

        subtitle_lbl = ctk.CTkLabel(
            top_frame,
            text="Test ve simülasyon için 14 farklı uçuş/hata senaryosu • v1.4.0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_lbl.pack(side="left", padx=10, pady=12)

        main_content = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Sol Panel
        self.left_panel = ctk.CTkFrame(main_content, width=440, corner_radius=10, border_width=1, border_color="#2b3035")
        self.left_panel.pack(side="left", fill="y", padx=(0, 10), pady=0)
        self.left_panel.pack_propagate(False)

        ctk.CTkLabel(self.left_panel, text="📌 Senaryo Seçimi:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(12, 5))

        self.scenario_keys = list(SCENARIO_DESCRIPTIONS.keys())
        self.scenario_values = list(SCENARIO_DESCRIPTIONS.values())

        self.combo_scenarios = ctk.CTkComboBox(
            self.left_panel,
            values=self.scenario_values,
            width=400,
            command=self._on_scenario_changed
        )
        self.combo_scenarios.set(self.scenario_values[0])
        self.combo_scenarios.pack(padx=15, pady=5)

        self.lbl_scenario_desc = ctk.CTkLabel(
            self.left_panel,
            text="Seçili senaryo açıklaması burada görünecek.",
            font=ctk.CTkFont(size=11),
            text_color="#ced4da",
            wraplength=400,
            justify="left"
        )
        self.lbl_scenario_desc.pack(anchor="w", padx=15, pady=(2, 12))

        ctk.CTkLabel(self.left_panel, text="⚙️ Parametre Ayarları:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(5, 5))

        p_row1 = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        p_row1.pack(fill="x", padx=15, pady=3)
        ctk.CTkLabel(p_row1, text="Kayıt Sayısı (Satır):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.entry_count = ctk.CTkEntry(p_row1, width=80)
        self.entry_count.insert(0, "60")
        self.entry_count.pack(side="right")

        p_row2 = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        p_row2.pack(fill="x", padx=15, pady=3)
        ctk.CTkLabel(p_row2, text="Kesinti Süresi (sn):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.entry_gap = ctk.CTkEntry(p_row2, width=80)
        self.entry_gap.insert(0, "12.0")
        self.entry_gap.pack(side="right")

        p_row3 = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        p_row3.pack(fill="x", padx=15, pady=3)
        ctk.CTkLabel(p_row3, text="Başlangıç İrtifası (m):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.entry_alt = ctk.CTkEntry(p_row3, width=80)
        self.entry_alt.insert(0, "100.0")
        self.entry_alt.pack(side="right")

        p_row4 = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        p_row4.pack(fill="x", padx=15, pady=3)
        ctk.CTkLabel(p_row4, text="Başlangıç Hızı (m/s):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.entry_spd = ctk.CTkEntry(p_row4, width=80)
        self.entry_spd.insert(0, "15.0")
        self.entry_spd.pack(side="right")

        p_row5 = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        p_row5.pack(fill="x", padx=15, pady=3)
        ctk.CTkLabel(p_row5, text="Başlangıç Batarya (%):", font=ctk.CTkFont(size=12)).pack(side="left")
        self.entry_bat = ctk.CTkEntry(p_row5, width=80)
        self.entry_bat.insert(0, "100.0")
        self.entry_bat.pack(side="right")

        # İşlemler
        ctk.CTkLabel(self.left_panel, text="🚀 Üretim İşlemleri:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))

        self.btn_preview = ctk.CTkButton(
            self.left_panel,
            text="👁️ Veriyi Canlı Önizle",
            command=self.preview_data_action,
            fg_color="#1971c2",
            hover_color="#1864ab",
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_preview.pack(fill="x", padx=15, pady=5)

        self.btn_save_csv = ctk.CTkButton(
            self.left_panel,
            text="💾 Seçili Senaryoyu Farklı Kaydet",
            command=self.save_csv_action,
            fg_color="#2b8a3e",
            hover_color="#237032",
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_save_csv.pack(fill="x", padx=15, pady=5)

        self.btn_batch_export = ctk.CTkButton(
            self.left_panel,
            text="📦 Tüm Senaryoları Yeni Periyot Klasöründe Üret",
            command=self.batch_export_action,
            fg_color="#7048e8",
            hover_color="#5f3dc4",
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_batch_export.pack(fill="x", padx=15, pady=5)

        self.btn_open_samples = ctk.CTkButton(
            self.left_panel,
            text="📁 Üretilen Klasörleri Aç",
            command=self.open_samples_folder,
            fg_color="#495057",
            hover_color="#343a40"
        )
        self.btn_open_samples.pack(fill="x", padx=15, pady=5)

        # Sağ Panel (Sekmeli: Tablo Önizleme & Ham CSV Metin Görünümü + Sayfa Geçiş Animasyonu)
        right_panel = ctk.CTkFrame(main_content, corner_radius=10, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=0, pady=0)

        preview_header = ctk.CTkFrame(right_panel, corner_radius=10)
        preview_header.pack(fill="x", padx=0, pady=(0, 8))

        ctk.CTkLabel(
            preview_header,
            text="📊 Canlı Telemetri Veri Önizlemesi",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="left", padx=15, pady=10)

        self.lbl_stats = ctk.CTkLabel(
            preview_header,
            text="Önizleme hazır değil",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        self.lbl_stats.pack(side="right", padx=15, pady=10)

        self.tabview = ctk.CTkTabview(
            right_panel,
            corner_radius=10,
            border_width=2,
            border_color="#2b3035",
            command=self._on_tab_switched
        )
        self.tabview.pack(fill="both", expand=True)

        self.tab_table = self.tabview.add("📋 Tablo Görünümü")
        self.tab_raw = self.tabview.add("📄 Ham CSV İçeriği (Raw)")
        self.tab_info = self.tabview.add("ℹ️ Senaryo Rehberi")

        # Sekme 1: Tablo
        table_frame = ctk.CTkFrame(self.tab_table, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.columns = ("timestamp", "altitude", "speed", "battery_pct", "longitude", "latitude", "pitch", "roll", "yaw")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#212529", foreground="white", fieldbackground="#212529", rowheight=24)
        style.configure("Treeview.Heading", background="#343a40", foreground="white", font=('Helvetica', 10, 'bold'))
        style.map("Treeview", background=[('selected', '#2b8a3e')])

        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # Sekme 2: Ham CSV Metni
        self.txt_raw = ctk.CTkTextbox(self.tab_raw, font=ctk.CTkFont(family="Consolas", size=12))
        self.txt_raw.pack(fill="both", expand=True, padx=10, pady=10)

        # Sekme 3: Senaryo Rehberi
        info_txt = ctk.CTkTextbox(self.tab_info, font=ctk.CTkFont(size=13))
        info_txt.pack(fill="both", expand=True, padx=10, pady=10)
        guide_lines = ["🧪 14 FARKLI İHA TELEMETRİ SENARYOSU REHBERİ\n" + "=" * 55 + "\n"]
        for idx, (k, v) in enumerate(SCENARIO_DESCRIPTIONS.items(), 1):
            guide_lines.append(f"{idx:02d}. [{k}]\n    • {v}\n")
        info_txt.insert("1.0", "\n".join(guide_lines))
        info_txt.configure(state="disabled")

        self._on_scenario_changed(self.combo_scenarios.get())
        self.preview_data_action()

    def _on_tab_switched(self):
        """Sayfa geçişlerinde yeşil çerçeve parlaması (glow pulse) animasyonu."""
        glow_colors = ["#2bda72", "#40c057", "#2b8a3e", "#2b3035"]

        def animate_border(idx=0):
            if idx < len(glow_colors):
                self.tabview.configure(border_color=glow_colors[idx])
                self.after(65, animate_border, idx + 1)

        animate_border(0)

    def _get_selected_scenario_key(self) -> str:
        idx = self.combo_scenarios.cget("values").index(self.combo_scenarios.get())
        return self.scenario_keys[idx]

    def _on_scenario_changed(self, choice):
        key = self._get_selected_scenario_key()
        desc = SCENARIO_DESCRIPTIONS.get(key, "")
        self.lbl_scenario_desc.configure(text=f"Açıklama: {desc}")
        self._on_tab_switched()

    def _read_params(self):
        try:
            count = int(self.entry_count.get().strip())
            gap = float(self.entry_gap.get().strip())
            alt = float(self.entry_alt.get().strip())
            spd = float(self.entry_spd.get().strip())
            bat = float(self.entry_bat.get().strip())
            if count <= 0:
                raise ValueError
            return count, gap, alt, spd, bat
        except Exception:
            messagebox.showerror("Hatalı Giriş", "Lütfen tüm parametre alanlarına geçerli sayısal değerler giriniz!")
            return None

    def preview_data_action(self):
        params = self._read_params()
        if not params:
            return

        count, gap, alt, spd, bat = params
        key = self._get_selected_scenario_key()

        df, raw = self.generator.generate_data(
            scenario_key=key,
            count=count,
            gap_duration_sec=gap,
            initial_altitude=alt,
            initial_speed=spd,
            initial_battery=bat
        )
        self.current_df = df
        self.current_raw = raw

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.txt_raw.configure(state="normal")
        self.txt_raw.delete("1.0", "end")

        if df is not None and not df.empty:
            for _, row in df.iterrows():
                vals = [row.get(col, "") for col in self.columns]
                self.tree.insert("", "end", values=vals)
            csv_text = df.to_csv(index=False)
            self.txt_raw.insert("1.0", csv_text)
            self._animate_row_counter(len(df))
        elif raw is not None:
            self.txt_raw.insert("1.0", raw if raw else "<0 Bayt Boş Dosya>")
            self.lbl_stats.configure(
                text="Özel Ham/Bozuk Metin Formatı (Ham CSV Sekmesine Bakınız)",
                text_color="#ff6b6b"
            )
        else:
            self.lbl_stats.configure(
                text="0 Bayt Boş Dosya Senaryosu",
                text_color="#fcc419"
            )

        self.txt_raw.configure(state="disabled")
        self._on_tab_switched()

    def _animate_row_counter(self, target_count: int):
        """Üretilen satır sayısını sayaç animasyonuyla gösterir."""
        steps = 10

        def step(s=1):
            if s >= steps:
                self.lbl_stats.configure(
                    text=f"⚡ {target_count} kayıt üretildi • Durum: Önizleme Hazır",
                    text_color="#51cf66"
                )
                return
            val = int((target_count / steps) * s)
            self.lbl_stats.configure(
                text=f"⏳ {val} kayıt üretiliyor...",
                text_color="#2bda72"
            )
            self.after(20, step, s + 1)

        step(1)

    def save_csv_action(self):
        params = self._read_params()
        if not params:
            return

        count, gap, alt, spd, bat = params
        key = self._get_selected_scenario_key()

        time_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{time_tag}_telemetry_{key}.csv"

        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".csv",
            filetypes=[("CSV Dosyaları", "*.csv"), ("Tüm Dosyalar", "*.*")]
        )
        if not file_path:
            return

        try:
            self.generator.generate_and_save(
                scenario_key=key,
                output_file_path=file_path,
                count=count,
                gap_duration_sec=gap,
                initial_altitude=alt,
                initial_speed=spd,
                initial_battery=bat
            )
            messagebox.showinfo(
                "Kayıt Başarılı",
                f"CSV dosyası başarıyla kaydedildi:\n\n{file_path}"
            )
        except Exception as e:
            messagebox.showerror("Kayıt Hatası", f"Dosya kaydedilirken hata oluştu:\n{str(e)}")

    def batch_export_action(self):
        """14 senaryoyu sıralı ve tarihli izole bir periyot klasöründe üretir."""
        params = self._read_params()
        if not params:
            return
        count, gap, alt, spd, bat = params

        target_base = filedialog.askdirectory(
            title="Periyot Klasörünün Oluşturulacağı Ana Dizini Seçin",
            initialdir=os.path.abspath("samples") if os.path.exists("samples") else os.getcwd()
        )
        if not target_base:
            return

        try:
            batch_dir = self.generator.generate_isolated_batch(
                base_output_dir=target_base,
                count=count,
                gap_duration_sec=gap,
                initial_altitude=alt,
                initial_speed=spd,
                initial_battery=bat
            )
            messagebox.showinfo(
                "Toplu Üretim Tamamlandı",
                f"Tüm senaryolar sıralı ve tarihli yeni klasörde izole edildi:\n\n{batch_dir}\n\n"
                f"Bu klasördeki dosyaları doğrudan analiz uygulamasına yükleyebilirsiniz."
            )
        except Exception as e:
            messagebox.showerror("Hata", f"Toplu üretim sırasında hata oluştu:\n{str(e)}")

    def open_samples_folder(self):
        sample_dir = os.path.abspath("samples")
        if not os.path.exists(sample_dir):
            os.makedirs(sample_dir, exist_ok=True)
        os.startfile(sample_dir)


if __name__ == "__main__":
    app = CSVGeneratorApp()
    app.mainloop()
