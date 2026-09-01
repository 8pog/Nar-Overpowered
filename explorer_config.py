import customtkinter as ctk
import os
import winreg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# المسارات ومفاتيح الريجستري
PATHS = {
    "RegAdv": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
    "RegExp": r"Software\Microsoft\Windows\CurrentVersion\Explorer",
    "RegDeskIcons": r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
    "ClsidHome": r"Software\Classes\CLSID\{f874310e-b6b7-47dc-bc84-b9e6b38f5903}",
    "ClsidGallery": r"Software\Classes\CLSID\{e88865ea-0e1c-4e20-9aa6-edcd0212c87c}",
    "ClsidNetwork": r"Software\Classes\CLSID\{F02C1A0D-BE21-4350-88B0-7367FC96EF3C}",
    "ClsidRecycle": r"Software\Classes\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}",
    "ClsidMenu": r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}"
}

# قاموس الترجمة (الحالة ON تعني الزر أخضر، الحالة OFF تعني الزر رمادي)
TRANSLATIONS = {
    "en": {
        "title": "EXPLORER CONFIGURATION",
        "subtitle": "By Developer Nar",
        "nav_title": "Navigation Settings",
        "ui_title": "Interface Settings",
        "btn_apply": "Apply All Changes",
        "btn_restart": "Restart Explorer",
        "applied_msg": "Applied Successfully!",
        "lang_btn": "عربي",
        "settings": {
            "OpenLoc": {"title": "Open Explorer to", "desc": "Sets default view when opening File Explorer.", "on": "This PC", "off": "Home"},
            "Home": {"title": "Home Button", "desc": "Shows or hides the Home icon in navigation pane.", "on": "Hidden", "off": "Visible"},
            "Gallery": {"title": "Gallery Button", "desc": "Shows or hides the Gallery icon in navigation pane.", "on": "Hidden", "off": "Visible"},
            "Network": {"title": "Network Button", "desc": "Shows or hides the Network icon in navigation pane.", "on": "Hidden", "off": "Visible"},
            "RecycleNav": {"title": "Recycle Bin (Nav)", "desc": "Shows Recycle Bin in the left sidebar.", "on": "Visible", "off": "Hidden"},
            "DeskRecycle": {"title": "Desktop Recycle Bin", "desc": "Shows Recycle Bin on the Desktop.", "on": "Hidden", "off": "Visible"},
            "Compact": {"title": "Compact View", "desc": "Decreases space between items in Explorer.", "on": "Enabled", "off": "Disabled"},
            "Privacy": {"title": "Privacy (Recent)", "desc": "Tracks and shows recently opened files.", "on": "Disabled", "off": "Enabled"},
            "CtxMenu": {"title": "Context Menu", "desc": "Restores the Windows 10 classic right-click menu.", "on": "Classic", "off": "Modern"},
        }
    },
    "ar": {
        "title": "إعدادات مستكشف الملفات",
        "subtitle": "بواسطة المطور نار (Developer Nar)",
        "nav_title": "إعدادات التنقل",
        "ui_title": "إعدادات الواجهة",
        "btn_apply": "تطبيق التغييرات",
        "btn_restart": "إعادة تشغيل المتصفح",
        "applied_msg": "تم التطبيق بنجاح!",
        "lang_btn": "English",
        "settings": {
            "OpenLoc": {"title": "فتح المتصفح على", "desc": "يحدد الواجهة الافتراضية عند فتح مستكشف الملفات.", "on": "هذا الكمبيوتر", "off": "الرئيسية"},
            "Home": {"title": "زر الرئيسية (Home)", "desc": "إظهار أو إخفاء أيقونة الرئيسية في القائمة الجانبية.", "on": "مخفي", "off": "مرئي"},
            "Gallery": {"title": "زر المعرض (Gallery)", "desc": "إظهار أو إخفاء أيقونة المعرض في القائمة الجانبية.", "on": "مخفي", "off": "مرئي"},
            "Network": {"title": "زر الشبكة (Network)", "desc": "إظهار أو إخفاء أيقونة الشبكة في القائمة الجانبية.", "on": "مخفي", "off": "مرئي"},
            "RecycleNav": {"title": "سلة المحذوفات (القائمة)", "desc": "إظهار سلة المحذوفات في القائمة الجانبية.", "on": "مرئي", "off": "مخفي"},
            "DeskRecycle": {"title": "سلة المحذوفات (سطح المكتب)", "desc": "إظهار سلة المحذوفات على سطح المكتب.", "on": "مخفي", "off": "مرئي"},
            "Compact": {"title": "العرض المضغوط", "desc": "تقليل المسافة بين العناصر في المتصفح.", "on": "مفعل", "off": "معطل"},
            "Privacy": {"title": "الخصوصية (الملفات الحديثة)", "desc": "تتبع وإظهار الملفات التي تم فتحها مؤخراً.", "on": "معطل", "off": "مفعل"},
            "CtxMenu": {"title": "القائمة الكلاسيكية", "desc": "استعادة قائمة الكليك يمين الكلاسيكية الخاصة بويندوز 10.", "on": "كلاسيكي", "off": "حديث"},
        }
    }
}

def get_reg_value(key_path, value_name, default_val):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return val
    except WindowsError:
        return default_val

class ExplorerConfigApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.lang = "en"
        self.settings = {}
        self.ui_elements = {}

        self.title("Explorer Config - Developer Nar")
        self.geometry("680x750")
        self.resizable(False, False)

        font_title = ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        font_sub = ctk.CTkFont(family="Segoe UI", size=14)

        # الإطار العلوي
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(15, 5), padx=20)
        
        self.header_frame.columnconfigure(0, weight=1)
        self.header_frame.columnconfigure(1, weight=1)
        self.header_frame.columnconfigure(2, weight=1)

        self.title_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.title_container.grid(row=0, column=1)

        self.title_label = ctk.CTkLabel(self.title_container, text=TRANSLATIONS[self.lang]["title"], font=font_title, text_color="#00FFFF")
        self.title_label.pack()
        self.subtitle = ctk.CTkLabel(self.title_container, text=TRANSLATIONS[self.lang]["subtitle"], font=font_sub, text_color="#FACC15")
        self.subtitle.pack(pady=(5, 0))

        # زر اللغة
        self.btn_lang = ctk.CTkButton(self.header_frame, text=TRANSLATIONS[self.lang]["lang_btn"], width=60, height=30, fg_color="#374151", hover_color="#1F2937", command=self.toggle_language)
        self.btn_lang.grid(row=0, column=2, sticky="ne")

        self.main_frame = ctk.CTkScrollableFrame(self, width=620, height=520, fg_color="transparent")
        self.main_frame.pack(padx=20, pady=5, fill="both", expand=True)

        # --- قراءة حالة النظام الفعلية وإضافة الإعدادات ---
        self.nav_title_lbl = self.create_section_title(TRANSLATIONS[self.lang]["nav_title"])
        
        self.add_setting("OpenLoc", get_reg_value(PATHS["RegAdv"], "LaunchTo", 2) == 1)
        self.add_setting("Home", get_reg_value(PATHS["ClsidHome"], "System.IsPinnedToNameSpaceTree", 1) == 0)
        self.add_setting("Gallery", get_reg_value(PATHS["ClsidGallery"], "System.IsPinnedToNameSpaceTree", 1) == 0)
        self.add_setting("Network", get_reg_value(PATHS["ClsidNetwork"], "System.IsPinnedToNameSpaceTree", 1) == 0)

        self.ui_title_lbl = self.create_section_title(TRANSLATIONS[self.lang]["ui_title"])

        self.add_setting("RecycleNav", get_reg_value(PATHS["ClsidRecycle"], "System.IsPinnedToNameSpaceTree", 0) == 1)
        self.add_setting("DeskRecycle", get_reg_value(PATHS["RegDeskIcons"], "{645FF040-5081-101B-9F08-00AA002F954E}", 0) == 1)
        self.add_setting("Compact", get_reg_value(PATHS["RegAdv"], "UseCompactMode", 0) == 1)
        self.add_setting("Privacy", get_reg_value(PATHS["RegExp"], "ShowRecent", 1) == 0)

        ctx_exists = True
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, PATHS["ClsidMenu"] + r"\InprocServer32", 0, winreg.KEY_READ)
        except WindowsError:
            ctx_exists = False
        self.add_setting("CtxMenu", ctx_exists)

        # الإطار السفلي (الأزرار)
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(pady=15, fill="x")

        self.btn_apply = ctk.CTkButton(self.bottom_frame, text=TRANSLATIONS[self.lang]["btn_apply"], fg_color="#10B981", hover_color="#059669", font=font_title, command=self.apply_changes)
        self.btn_apply.pack(side="left", padx=20, expand=True)

        self.btn_restart = ctk.CTkButton(self.bottom_frame, text=TRANSLATIONS[self.lang]["btn_restart"], fg_color="#F59E0B", hover_color="#D97706", font=font_title, command=self.restart_explorer)
        self.btn_restart.pack(side="left", padx=20, expand=True)

    def create_section_title(self, text):
        lbl = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#9CA3AF")
        lbl.pack(anchor="w", pady=(15, 5))
        return lbl

    def add_setting(self, key, initial_state):
        row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=10)

        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        t_data = TRANSLATIONS[self.lang]["settings"][key]
        
        title_lbl = ctk.CTkLabel(info_frame, text=t_data["title"], font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        title_lbl.pack(anchor="w")
        desc_lbl = ctk.CTkLabel(info_frame, text=t_data["desc"], font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#6B7280")
        desc_lbl.pack(anchor="w")

        var = ctk.BooleanVar(value=initial_state)
        status_lbl = ctk.CTkLabel(row, width=80, font=ctk.CTkFont(family="Segoe UI", weight="bold"))
        status_lbl.pack(side="right", padx=(10, 0))

        self.settings[key] = var
        self.ui_elements[key] = {
            "title": title_lbl, "desc": desc_lbl, "status": status_lbl
        }

        def on_change(*args, k=key):
            self.refresh_status_label(k)
            
        var.trace_add("write", on_change)
        self.refresh_status_label(key)

        switch = ctk.CTkSwitch(row, text="", variable=var, width=40, progress_color="#10B981")
        switch.pack(side="right")

    def refresh_status_label(self, key):
        state = self.settings[key].get()
        el = self.ui_elements[key]
        t = TRANSLATIONS[self.lang]["settings"][key]
        
        # ربط مباشر: الزر شغال = نص الأون + لون أخضر / الزر مطفي = نص الأوف + لون أحمر
        el["status"].configure(text=t["on"] if state else t["off"])
        el["status"].configure(text_color="#10B981" if state else "#EF4444")

    def toggle_language(self):
        self.lang = "ar" if self.lang == "en" else "en"
        t = TRANSLATIONS[self.lang]
        
        self.btn_lang.configure(text=t["lang_btn"])
        self.title_label.configure(text=t["title"])
        self.subtitle.configure(text=t["subtitle"])
        self.nav_title_lbl.configure(text=t["nav_title"])
        self.ui_title_lbl.configure(text=t["ui_title"])
        self.btn_apply.configure(text=t["btn_apply"])
        self.btn_restart.configure(text=t["btn_restart"])
        
        for key, el in self.ui_elements.items():
            st = t["settings"][key]
            el["title"].configure(text=st["title"])
            el["desc"].configure(text=st["desc"])
            self.refresh_status_label(key)

    def apply_changes(self):
        HKCU = "HKCU\\"
        
        v = "1" if self.settings["OpenLoc"].get() else "2"
        os.system(f'reg add "{HKCU}{PATHS["RegAdv"]}" /v LaunchTo /t REG_DWORD /d {v} /f >nul 2>&1')
        
        v = "0" if self.settings["Home"].get() else "1"
        os.system(f'reg add "{HKCU}{PATHS["ClsidHome"]}" /v System.IsPinnedToNameSpaceTree /t REG_DWORD /d {v} /f >nul 2>&1')

        v = "0" if self.settings["Gallery"].get() else "1"
        os.system(f'reg add "{HKCU}{PATHS["ClsidGallery"]}" /v System.IsPinnedToNameSpaceTree /t REG_DWORD /d {v} /f >nul 2>&1')

        v = "0" if self.settings["Network"].get() else "1"
        os.system(f'reg add "{HKCU}{PATHS["ClsidNetwork"]}" /v System.IsPinnedToNameSpaceTree /t REG_DWORD /d {v} /f >nul 2>&1')

        v = "1" if self.settings["RecycleNav"].get() else "0"
        os.system(f'reg add "{HKCU}{PATHS["ClsidRecycle"]}" /v System.IsPinnedToNameSpaceTree /t REG_DWORD /d {v} /f >nul 2>&1')

        if self.settings["DeskRecycle"].get():
            os.system(f'reg add "{HKCU}{PATHS["RegDeskIcons"]}" /v "{{645FF040-5081-101B-9F08-00AA002F954E}}" /t REG_DWORD /d 1 /f >nul 2>&1')
        else:
            os.system(f'reg delete "{HKCU}{PATHS["RegDeskIcons"]}" /v "{{645FF040-5081-101B-9F08-00AA002F954E}}" /f >nul 2>&1')

        v = "1" if self.settings["Compact"].get() else "0"
        os.system(f'reg add "{HKCU}{PATHS["RegAdv"]}" /v UseCompactMode /t REG_DWORD /d {v} /f >nul 2>&1')

        v = "0" if self.settings["Privacy"].get() else "1"
        os.system(f'reg add "{HKCU}{PATHS["RegExp"]}" /v ShowRecent /t REG_DWORD /d {v} /f >nul 2>&1')
        os.system(f'reg add "{HKCU}{PATHS["RegExp"]}" /v ShowFrequent /t REG_DWORD /d {v} /f >nul 2>&1')
        os.system(f'reg add "{HKCU}{PATHS["RegExp"]}" /v ShowCloudFilesInQuickAccess /t REG_DWORD /d {v} /f >nul 2>&1')

        if self.settings["CtxMenu"].get():
            os.system(f'reg add "{HKCU}{PATHS["ClsidMenu"]}\\InprocServer32" /ve /f >nul 2>&1')
        else:
            os.system(f'reg delete "{HKCU}{PATHS["ClsidMenu"]}" /f >nul 2>&1')

        self.btn_apply.configure(text=TRANSLATIONS[self.lang]["applied_msg"], fg_color="#047857")
        self.after(2000, lambda: self.btn_apply.configure(text=TRANSLATIONS[self.lang]["btn_apply"], fg_color="#10B981"))

    def restart_explorer(self):
        os.system("taskkill /f /im explorer.exe >nul 2>&1")
        os.system("start explorer.exe")

if __name__ == "__main__":
    app = ExplorerConfigApp()
    app.mainloop()
