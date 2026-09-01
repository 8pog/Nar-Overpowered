import customtkinter as ctk
import os
import winreg
import ctypes
import sys
import threading

# 1. طلب صلاحيات المسؤول بصمت
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    script_path = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
    sys.exit()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# دالة قراءة الريجستري المعدلة
def get_reg_value(hive, key_path, value_name, default_val):
    try:
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return val
    except:
        return default_val

# 2. قاموس الترجمة المبني على "حالة الميزة" وليس "حالة الأداة"
TRANSLATIONS = {
    "en": {
        "title": "WINDOWS AI MANAGER",
        "subtitle": "By Developer Nar",
        "cat_core": "Core System AI",
        "cat_apps": "App-Specific AI",
        "cat_priv": "Privacy & Data Harvesting",
        "btn_apply": "Apply Changes",
        "btn_restore": "Enable All AI (Defaults)",
        "btn_restart": "Restart Explorer",
        "applied_msg": "Applied Successfully!",
        "lang_btn": "عربي",
        "settings": {
            "Copilot": {"title": "Windows Copilot", "desc": "Windows built-in AI assistant & taskbar icon.", "on": "Enabled", "off": "Disabled"},
            "Recall": {"title": "Recall AI", "desc": "AI screen capture and background data analysis.", "on": "Enabled", "off": "Disabled"},
            "EdgeCopilot": {"title": "Copilot in Edge", "desc": "Copilot and Discover sidebar in MS Edge.", "on": "Enabled", "off": "Disabled"},
            "GamingCopilot": {"title": "Gaming Copilot", "desc": "AI features integrated into Windows Gaming.", "on": "Enabled", "off": "Disabled"},
            "AIActions": {"title": "OS AI Actions", "desc": "Predictive AI actions and system interactions.", "on": "Enabled", "off": "Disabled"},
            
            "PaintAI": {"title": "Paint AI Experiments", "desc": "AI image generation features in MS Paint.", "on": "Enabled", "off": "Disabled"},
            "OfficeCopilot": {"title": "Office Copilot", "desc": "AI integrations in Word, Excel, and PowerPoint.", "on": "Enabled", "off": "Disabled"},
            "PhotosAI": {"title": "Photos AI Features", "desc": "Smart AI editing tools in the Photos app.", "on": "Enabled", "off": "Disabled"},
            "SnippingAI": {"title": "Click to Do (Snipping)", "desc": "AI text and image actions in Snipping Tool.", "on": "Enabled", "off": "Disabled"},
            
            "InputInsights": {"title": "Typing Data Harvesting", "desc": "Collects typing behavior for AI predictions.", "on": "Enabled", "off": "Disabled"},
            "AIFabric": {"title": "AI Fabric Service", "desc": "Background service supporting Windows AI.", "on": "Enabled", "off": "Disabled"},
            "VoiceAccess": {"title": "Voice Access", "desc": "AI-powered voice dictation and control.", "on": "Enabled", "off": "Disabled"},
            "VoiceEffects": {"title": "AI Voice Effects", "desc": "AI audio enhancements and background noise removal.", "on": "Enabled", "off": "Disabled"},
            "SettingsAI": {"title": "Settings AI Search", "desc": "AI search suggestions within Windows Settings.", "on": "Enabled", "off": "Disabled"}
        }
    },
    "ar": {
        "title": "إدارة الذكاء الاصطناعي",
        "subtitle": "By Developer Nar",
        "cat_core": "الذكاء الاصطناعي للنظام",
        "cat_apps": "تطبيقات الذكاء الاصطناعي",
        "cat_priv": "الخصوصية وجمع البيانات",
        "btn_apply": "تطبيق التعديلات",
        "btn_restore": "تفعيل الكل (الافتراضي)",
        "btn_restart": "إعادة تشغيل المتصفح",
        "applied_msg": "تم التطبيق بنجاح!",
        "lang_btn": "English",
        "settings": {
            "Copilot": {"title": "مساعد الويندوز (Copilot)", "desc": "مساعد الذكاء الاصطناعي المدمج في النظام.", "on": "مفعل", "off": "معطل"},
            "Recall": {"title": "ميزة الاسترجاع (Recall)", "desc": "تصوير الشاشة وتحليل البيانات بالخلفية.", "on": "مفعل", "off": "معطل"},
            "EdgeCopilot": {"title": "كوبايلوت في إيدج", "desc": "شريط الذكاء الاصطناعي الجانبي في المتصفح.", "on": "مفعل", "off": "معطل"},
            "GamingCopilot": {"title": "كوبايلوت الألعاب", "desc": "ميزات الذكاء الاصطناعي المدمجة في الألعاب.", "on": "مفعل", "off": "معطل"},
            "AIActions": {"title": "إجراءات النظام الذكية", "desc": "تفاعلات وتوقعات النظام المبنية على الذكاء.", "on": "مفعل", "off": "معطل"},
            
            "PaintAI": {"title": "الذكاء الاصطناعي في الرسام", "desc": "ميزة التوليد الذكي للصور في برنامج الرسام.", "on": "مفعل", "off": "معطل"},
            "OfficeCopilot": {"title": "كوبايلوت في أوفيس", "desc": "مساعد الذكاء الاصطناعي في تطبيقات Office.", "on": "مفعل", "off": "معطل"},
            "PhotosAI": {"title": "الذكاء الاصطناعي في الصور", "desc": "أدوات التعديل الذكية في تطبيق الصور.", "on": "مفعل", "off": "معطل"},
            "SnippingAI": {"title": "ميزة Click to Do", "desc": "التفاعل الذكي مع النصوص في أداة القطع.", "on": "مفعل", "off": "معطل"},
            
            "InputInsights": {"title": "جمع بيانات الكتابة", "desc": "تحليل وجمع بيانات الكتابة لتحسين التوقعات.", "on": "مفعل", "off": "معطل"},
            "AIFabric": {"title": "خدمة AI Fabric", "desc": "خدمات الذكاء الاصطناعي التي تعمل في الخلفية.", "on": "مفعل", "off": "معطل"},
            "VoiceAccess": {"title": "الوصول الصوتي", "desc": "التحكم وإملاء النصوص باستخدام الذكاء الاصطناعي.", "on": "مفعل", "off": "معطل"},
            "VoiceEffects": {"title": "تأثيرات الصوت الذكية", "desc": "تحسينات وتنقية الصوت بالذكاء الاصطناعي.", "on": "مفعل", "off": "معطل"},
            "SettingsAI": {"title": "الذكاء الاصطناعي بالإعدادات", "desc": "الاقتراحات الذكية في بحث إعدادات الويندوز.", "on": "مفعل", "off": "معطل"}
        }
    }
}

class FullAIRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.lang = "en"
        self.settings = {}
        self.ui_elements = {}

        self.title("Windows AI Manager - Developer Nar")
        self.geometry("750x850")
        self.resizable(False, False)

        font_title = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        font_sub = ctk.CTkFont(family="Segoe UI", size=14)

        # Header
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

        self.btn_lang = ctk.CTkButton(self.header_frame, text=TRANSLATIONS[self.lang]["lang_btn"], width=60, height=30, fg_color="#374151", hover_color="#1F2937", command=self.toggle_language)
        self.btn_lang.grid(row=0, column=2, sticky="ne")

        # Main Frame
        self.main_frame = ctk.CTkScrollableFrame(self, width=680, height=550, fg_color="transparent")
        self.main_frame.pack(padx=20, pady=5, fill="both", expand=True)

        HKCU = winreg.HKEY_CURRENT_USER
        HKLM = winreg.HKEY_LOCAL_MACHINE

        # --- Section 1: Core System AI ---
        self.lbl_core = self.create_section_title(TRANSLATIONS[self.lang]["cat_core"], "#FACC15")
        # True = ENABLED in Windows. False = DISABLED in Windows.
        self.add_setting("Copilot", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 0) != 1)
        self.add_setting("Recall", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\WindowsAI", "DisableAIDataAnalysis", 0) != 1)
        self.add_setting("EdgeCopilot", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Edge", "HubsSidebarEnabled", 1) != 0)
        self.add_setting("GamingCopilot", get_reg_value(HKCU, r"Software\Policies\Microsoft\Windows\Gaming", "DisableGamingCopilot", 0) != 1)
        self.add_setting("AIActions", get_reg_value(HKCU, r"Software\Policies\Microsoft\Windows\Explorer", "DisableAIActions", 0) != 1)

        # --- Section 2: Apps AI ---
        self.lbl_apps = self.create_section_title(TRANSLATIONS[self.lang]["cat_apps"], "#FACC15")
        self.add_setting("PaintAI", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\Paint", "DisableAI", 0) != 1)
        self.add_setting("OfficeCopilot", get_reg_value(HKCU, r"Software\Policies\Microsoft\Office\16.0\Common\Copilot", "TurnOffCopilot", 0) != 1)
        self.add_setting("PhotosAI", get_reg_value(HKCU, r"Software\Policies\Microsoft\Windows\Photos", "DisableAI", 0) != 1)
        self.add_setting("SnippingAI", get_reg_value(HKCU, r"Software\Policies\Microsoft\Windows\SnippingTool", "DisableClickToDo", 0) != 1)

        # --- Section 3: Privacy ---
        self.lbl_priv = self.create_section_title(TRANSLATIONS[self.lang]["cat_priv"], "#FACC15")
        self.add_setting("InputInsights", get_reg_value(HKCU, r"Software\Microsoft\Input\TIPC", "Enabled", 1) != 0)
        self.add_setting("AIFabric", get_reg_value(HKLM, r"SYSTEM\CurrentControlSet\Services\AIFabric", "Start", 3) != 4)
        self.add_setting("VoiceAccess", get_reg_value(HKCU, r"Software\Microsoft\Speech_OneCore\Settings\VoiceAccess", "Enabled", 1) != 0)
        self.add_setting("VoiceEffects", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\Audio", "DisableVoiceEffects", 0) != 1)
        self.add_setting("SettingsAI", get_reg_value(HKCU, r"Software\Microsoft\Windows\CurrentVersion\Search", "DisableAISearch", 0) != 1)

        # Bottom Frame
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(pady=10, fill="x")

        self.btn_apply = ctk.CTkButton(self.bottom_frame, text=TRANSLATIONS[self.lang]["btn_apply"], fg_color="#10B981", hover_color="#059669", font=font_title, height=45, command=self.apply_changes)
        self.btn_apply.pack(side="left", padx=20, expand=True)

        self.btn_restore = ctk.CTkButton(self.bottom_frame, text=TRANSLATIONS[self.lang]["btn_restore"], fg_color="#EF4444", hover_color="#DC2626", font=font_title, height=45, command=self.restore_defaults)
        self.btn_restore.pack(side="right", padx=20, expand=True)

        self.btn_restart = ctk.CTkButton(self, text=TRANSLATIONS[self.lang]["btn_restart"], fg_color="#F59E0B", hover_color="#D97706", font=ctk.CTkFont(weight="bold", size=16), height=35, command=self.restart_explorer)
        self.btn_restart.pack(pady=(5,10), padx=40, fill="x")

    def create_section_title(self, text, color="#9CA3AF"):
        lbl = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color=color)
        lbl.pack(anchor="w", pady=(15, 5))
        return lbl

    def add_setting(self, key, is_enabled):
        row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=10)
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        t_data = TRANSLATIONS[self.lang]["settings"][key]
        title_lbl = ctk.CTkLabel(info_frame, text=t_data["title"], font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        title_lbl.pack(anchor="w")
        desc_lbl = ctk.CTkLabel(info_frame, text=t_data["desc"], font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#6B7280")
        desc_lbl.pack(anchor="w")

        var = ctk.BooleanVar(value=is_enabled)
        status_lbl = ctk.CTkLabel(row, width=80, font=ctk.CTkFont(family="Segoe UI", weight="bold"))
        status_lbl.pack(side="right", padx=(10, 0))

        self.settings[key] = var
        self.ui_elements[key] = {"title": title_lbl, "desc": desc_lbl, "status": status_lbl}

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
        # True = Green = Enabled. False = Red = Disabled.
        el["status"].configure(text=t["on"] if state else t["off"])
        el["status"].configure(text_color="#10B981" if state else "#EF4444")

    def toggle_language(self):
        self.lang = "ar" if self.lang == "en" else "en"
        t = TRANSLATIONS[self.lang]
        
        self.title_label.configure(text=t["title"])
        self.subtitle.configure(text=t["subtitle"])
        self.btn_lang.configure(text=t["lang_btn"])
        
        self.lbl_core.configure(text=t["cat_core"])
        self.lbl_apps.configure(text=t["cat_apps"])
        self.lbl_priv.configure(text=t["cat_priv"])
        
        self.btn_apply.configure(text=t["btn_apply"])
        self.btn_restore.configure(text=t["btn_restore"])
        self.btn_restart.configure(text=t["btn_restart"])
        
        for key, el in self.ui_elements.items():
            st = t["settings"][key]
            el["title"].configure(text=st["title"])
            el["desc"].configure(text=st["desc"])
            self.refresh_status_label(key)

    def apply_changes(self):
        self.btn_apply.configure(state="disabled", text="Working...")
        
        def task():
            HKCU = "HKCU\\"
            HKLM = "HKLM\\"
            cmds = []

            # 1. Copilot
            if not self.settings["Copilot"].get(): # User turned it OFF (Disable)
                cmds.extend([
                    f'reg add "{HKCU}Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v TurnOffWindowsCopilot /t REG_DWORD /d 1 /f',
                    f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v TurnOffWindowsCopilot /t REG_DWORD /d 1 /f',
                    f'reg add "{HKCU}Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowCopilotButton /t REG_DWORD /d 0 /f'
                ])
            else: # User turned it ON (Enable)
                cmds.extend([
                    f'reg delete "{HKCU}Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v TurnOffWindowsCopilot /f',
                    f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v TurnOffWindowsCopilot /f',
                    f'reg add "{HKCU}Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowCopilotButton /t REG_DWORD /d 1 /f'
                ])

            # 2. Recall AI
            if not self.settings["Recall"].get():
                cmds.extend([
                    f'reg add "{HKCU}SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsAI" /v DisableAIDataAnalysis /t REG_DWORD /d 1 /f',
                    f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsAI" /v DisableAIDataAnalysis /t REG_DWORD /d 1 /f'
                ])
            else:
                cmds.extend([f'reg delete "{HKCU}SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsAI" /v DisableAIDataAnalysis /f', f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsAI" /v DisableAIDataAnalysis /f'])

            # 3. Edge Copilot
            if not self.settings["EdgeCopilot"].get(): cmds.append(f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Edge" /v HubsSidebarEnabled /t REG_DWORD /d 0 /f')
            else: cmds.append(f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Edge" /v HubsSidebarEnabled /f')

            # 4. Gaming Copilot
            if not self.settings["GamingCopilot"].get(): cmds.append(f'reg add "{HKCU}Software\\Policies\\Microsoft\\Windows\\Gaming" /v DisableGamingCopilot /t REG_DWORD /d 1 /f')
            else: cmds.append(f'reg delete "{HKCU}Software\\Policies\\Microsoft\\Windows\\Gaming" /v DisableGamingCopilot /f')

            # 5. AI Actions
            if not self.settings["AIActions"].get(): cmds.append(f'reg add "{HKCU}Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableAIActions /t REG_DWORD /d 1 /f')
            else: cmds.append(f'reg delete "{HKCU}Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableAIActions /f')

            # 6. Paint AI
            if not self.settings["PaintAI"].get(): cmds.append(f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\Paint" /v DisableAI /t REG_DWORD /d 1 /f')
            else: cmds.append(f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\Paint" /v DisableAI /f')

            # 7. Office Copilot
            if not self.settings["OfficeCopilot"].get(): cmds.append(f'reg add "{HKCU}Software\\Policies\\Microsoft\\Office\\16.0\\Common\\Copilot" /v TurnOffCopilot /t REG_DWORD /d 1 /f')
            else: cmds.append(f'reg delete "{HKCU}Software\\Policies\\Microsoft\\Office\\16.0\\Common\\Copilot" /v TurnOffCopilot /f')

            # 8. Photos AI
            if not self.settings["PhotosAI"].get(): cmds.append(f'reg add "{HKCU}Software\\Policies\\Microsoft\\Windows\\Photos" /v DisableAI /t REG_DWORD /d 1 /f')
            else: cmds.append(f'reg delete "{HKCU}Software\\Policies\\Microsoft\\Windows\\Photos" /v DisableAI /f')

            # 9. Snipping Tool
            if not self.settings["SnippingAI"].get(): cmds.append(f'reg add "{HKCU}Software\\Policies\\Microsoft\\Windows\\SnippingTool" /v DisableClickToDo /t REG_DWORD /d 1 /f')
            else: cmds.append(f'reg delete "{HKCU}Software\\Policies\\Microsoft\\Windows\\SnippingTool" /v DisableClickToDo /f')

            # 10. Input Insights
            if not self.settings["InputInsights"].get(): cmds.append(f'reg add "{HKCU}Software\\Microsoft\\Input\\TIPC" /v Enabled /t REG_DWORD /d 0 /f')
            else: cmds.append(f'reg delete "{HKCU}Software\\Microsoft\\Input\\TIPC" /v Enabled /f')

            # 11. AI Fabric Service
            if not self.settings["AIFabric"].get():
                cmds.extend(['sc config AIFabric start= disabled', 'sc stop AIFabric'])
            else:
                cmds.extend(['sc config AIFabric start= demand', 'sc start AIFabric'])

            # 12. Voice Access
            if not self.settings["VoiceAccess"].get(): cmds.append(f'reg add "{HKCU}Software\\Microsoft\\Speech_OneCore\\Settings\\VoiceAccess" /v Enabled /t REG_DWORD /d 0 /f')
            else: cmds.append(f'reg delete "{HKCU}Software\\Microsoft\\Speech_OneCore\\Settings\\VoiceAccess" /v Enabled /f')

            # 13. Voice Effects
            if not self.settings["VoiceEffects"].get(): cmds.append(f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\Audio" /v DisableVoiceEffects /t REG_DWORD /d 1 /f')
            else: cmds.append(f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\Audio" /v DisableVoiceEffects /f')

            # 14. Settings AI
            if not self.settings["SettingsAI"].get(): cmds.append(f'reg add "{HKCU}Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v DisableAISearch /t REG_DWORD /d 1 /f')
            else: cmds.append(f'reg delete "{HKCU}Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v DisableAISearch /f')

            for cmd in cmds:
                os.system(cmd + " >nul 2>&1")

            self.after(0, lambda: self.btn_apply.configure(state="normal", text=TRANSLATIONS[self.lang]["applied_msg"], fg_color="#047857"))
            self.after(2000, lambda: self.btn_apply.configure(text=TRANSLATIONS[self.lang]["btn_apply"], fg_color="#10B981"))

        threading.Thread(target=task, daemon=True).start()

    def restore_defaults(self):
        # تفعيل جميع الميزات (العودة لافتراضيات الويندوز)
        for key, var in self.settings.items():
            var.set(True)
        self.apply_changes()

    def restart_explorer(self):
        os.system("taskkill /f /im explorer.exe >nul 2>&1")
        os.system("start explorer.exe")

if __name__ == "__main__":
    try:
        app = FullAIRemoverApp()
        app.mainloop()
    except Exception as e:
        input(f"Error occurred: {e}\nPress Enter to close...")
