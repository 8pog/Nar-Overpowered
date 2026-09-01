import customtkinter as ctk
import os
import winreg
import subprocess
import ctypes
import sys
import threading

# 1. نظام طلب الصلاحيات المُعدّل (يحفظ المسار الأصلي لتجنب الإغلاق المفاجئ)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # جلب المسار الكامل للملف ووضعه بين علامات تنصيص لحل مشكلة المسافات
    script_path = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
    sys.exit()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

def get_reg_value(hive, key_path, value_name, default_val):
    try:
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return val
    except FileNotFoundError:
        return default_val
    except Exception:
        return default_val

def get_active_power_plan():
    try:
        out = subprocess.check_output("powercfg /getactivescheme", shell=True, text=True)
        if "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c" in out.lower() or "high" in out.lower(): return "High"
        if "e9a42b02-d5df-448d-aa00-03f14749eb61" in out.lower() or "ultimate" in out.lower(): return "Ultimate"
        return "Balanced"
    except: return "Balanced"

TRANSLATIONS = {
    "en": {
        "title": "SYSTEM TWEAKER",
        "subtitle": "By Developer Nar",
        "cat_perf": "Performance",
        "cat_priv": "Privacy & Security",
        "cat_ui": "Interface & UX",
        "btn_taskbar": "Clear Taskbar",
        "btn_cleanup": "System Cleanup",
        "btn_apply": "Apply All Tweaks",
        "btn_restore": "Restore Defaults",
        "btn_restart": "Restart Explorer",
        "applied_msg": "Applied Successfully!",
        "lang_btn": "عربي",
        "settings": {
            "Power": {"title": "Power Plan Mode", "desc": "Select Windows power management plan."},
            "BackApps": {"title": "Background UWP Apps", "desc": "Allow apps to run in the background.", "on": "Disabled", "off": "Enabled"},
            "DelOpt": {"title": "Delivery Optimization", "desc": "Windows update peer-to-peer sharing.", "on": "Disabled", "off": "Enabled"},
            "Edge": {"title": "Edge Startup Boost", "desc": "Pre-loads Edge in the background.", "on": "Disabled", "off": "Enabled"},
            "Hiber": {"title": "Hibernation", "desc": "Saves memory state to hard drive.", "on": "Disabled", "off": "Enabled"},
            "FastBoot": {"title": "Fast Startup", "desc": "Speeds up boot time (Not needed for SSDs).", "on": "Disabled", "off": "Enabled"},
            "Tele": {"title": "Telemetry & Ads", "desc": "Windows data collection and tracking.", "on": "Disabled", "off": "Enabled"},
            "Copilot": {"title": "Windows Copilot AI", "desc": "Built-in Windows AI assistant.", "on": "Disabled", "off": "Enabled"},
            "UAC": {"title": "User Account Control", "desc": "Prompts when apps request admin rights.", "on": "Disabled", "off": "Enabled"},
            "MenuDelay": {"title": "Menu Show Delay", "desc": "Delay time when hovering over menus.", "on": "Fast (20ms)", "off": "Default (400ms)"},
            "WallComp": {"title": "Wallpaper Compression", "desc": "Windows compresses desktop wallpapers.", "on": "Disabled (100%)", "off": "Enabled"},
            "RecSec": {"title": "Recommended Section", "desc": "Shows recent files in Start menu.", "on": "Hidden", "off": "Visible"},
            "Mouse": {"title": "Mouse Acceleration", "desc": "Enhance pointer precision feature.", "on": "Disabled", "off": "Enabled"},
            "Sticky": {"title": "Sticky Keys (Logoff)", "desc": "Accessibility shortcut prompts.", "on": "Disabled", "off": "Enabled"},
        }
    },
    "ar": {
        "title": "مُحسّن النظام",
        "subtitle": " By Developer Nar ",
        "cat_perf": "الأداء (Performance)",
        "cat_priv": "الخصوصية والأمان (Privacy)",
        "cat_ui": "الواجهة (Interface)",
        "btn_taskbar": "تنظيف شريط المهام",
        "btn_cleanup": "تنظيف مخلفات النظام",
        "btn_apply": "تطبيق التعديلات",
        "btn_restore": "استعادة الافتراضيات",
        "btn_restart": "إعادة تشغيل المتصفح",
        "applied_msg": "تم التطبيق بنجاح!",
        "lang_btn": "English",
        "settings": {
            "Power": {"title": "خطة الطاقة", "desc": "تحديد وضع استهلاك وأداء الطاقة للنظام."},
            "BackApps": {"title": "تطبيقات الخلفية", "desc": "تشغيل تطبيقات الويندوز في الخلفية.", "on": "معطل", "off": "مفعل"},
            "DelOpt": {"title": "تحسين التسليم (Delivery Opt)", "desc": "مشاركة تحديثات الويندوز مع أجهزة أخرى.", "on": "معطل", "off": "مفعل"},
            "Edge": {"title": "تسريع إقلاع Edge", "desc": "تحميل المتصفح مسبقاً في الخلفية.", "on": "معطل", "off": "مفعل"},
            "Hiber": {"title": "الإسبات (Hibernation)", "desc": "حفظ حالة النظام على القرص الصلب.", "on": "معطل", "off": "مفعل"},
            "FastBoot": {"title": "الإقلاع السريع (Fast Startup)", "desc": "تسريع التشغيل (غير ضروري لأقراص SSD).", "on": "معطل", "off": "مفعل"},
            "Tele": {"title": "التتبع والإعلانات (Telemetry)", "desc": "جمع بيانات الاستخدام والإعلانات في ويندوز.", "on": "معطل", "off": "مفعل"},
            "Copilot": {"title": "مساعد الذكاء الاصطناعي (Copilot)", "desc": "مساعد ويندوز الذكي المدمج.", "on": "معطل", "off": "مفعل"},
            "UAC": {"title": "التحكم في حساب المستخدم (UAC)", "desc": "تنبيهات الأمان عند تشغيل البرامج كمسؤول.", "on": "معطل", "off": "مفعل"},
            "MenuDelay": {"title": "تأخير ظهور القوائم", "desc": "سرعة استجابة القوائم عند تمرير الفأرة.", "on": "سريع (20ms)", "off": "افتراضي (400ms)"},
            "WallComp": {"title": "ضغط جودة الخلفيات", "desc": "تقليل جودة صور سطح المكتب للحجم.", "on": "معطل (جودة 100%)", "off": "مفعل"},
            "RecSec": {"title": "قسم الموصى به", "desc": "إظهار الملفات الحديثة في قائمة إبدأ.", "on": "مخفي", "off": "مرئي"},
            "Mouse": {"title": "تسريع الفأرة (Acceleration)", "desc": "ميزة دقة المؤشر الخاصة بويندوز.", "on": "معطل", "off": "مفعل"},
            "Sticky": {"title": "المفاتيح الثابتة (Sticky Keys)", "desc": "اختصارات وإشعارات سهولة الوصول.", "on": "معطل", "off": "مفعل"},
        }
    }
}

class SystemTweakerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.lang = "en"
        self.settings = {}
        self.ui_elements = {}

        self.title("System Tweaker - Developer Nar")
        self.geometry("700x800")
        self.resizable(False, False)

        font_title = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        font_sub = ctk.CTkFont(family="Segoe UI", size=14)

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

        self.main_frame = ctk.CTkScrollableFrame(self, width=640, height=500, fg_color="transparent")
        self.main_frame.pack(padx=20, pady=5, fill="both", expand=True)

        HKCU = winreg.HKEY_CURRENT_USER
        HKLM = winreg.HKEY_LOCAL_MACHINE

        # --- Performance ---
        self.lbl_perf = self.create_section_title(TRANSLATIONS[self.lang]["cat_perf"], "#FACC15")
        
        self.power_var = ctk.StringVar(value=get_active_power_plan())
        self.add_power_setting()
        
        self.add_setting("BackApps", get_reg_value(HKCU, r"Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications", "GlobalUserDisabled", 0) == 1)
        self.add_setting("DelOpt", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization", "DODownloadMode", 99) == 0)
        self.add_setting("Edge", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Edge", "StartupBoostEnabled", 99) == 0)
        self.add_setting("Hiber", get_reg_value(HKLM, r"SYSTEM\CurrentControlSet\Control\Power", "HibernateEnabled", 1) == 0)
        self.add_setting("FastBoot", get_reg_value(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Power", "HiberbootEnabled", 1) == 0)

        # --- Privacy & Security ---
        self.lbl_priv = self.create_section_title(TRANSLATIONS[self.lang]["cat_priv"], "#FACC15")
        
        self.add_setting("Tele", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 99) == 0)
        self.add_setting("Copilot", get_reg_value(HKCU, r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 0) == 1)
        self.add_setting("UAC", get_reg_value(HKLM, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "ConsentPromptBehaviorAdmin", 5) == 0)

        # --- Interface & UX ---
        self.lbl_ui = self.create_section_title(TRANSLATIONS[self.lang]["cat_ui"], "#FACC15")
        
        self.add_setting("MenuDelay", get_reg_value(HKCU, r"Control Panel\Desktop", "MenuShowDelay", "400") == "20")
        self.add_setting("WallComp", get_reg_value(HKCU, r"Control Panel\Desktop", "JPEGImportQuality", 0) == 100)
        self.add_setting("RecSec", get_reg_value(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\Explorer", "HideRecommendedSection", 0) == 1)
        self.add_setting("Mouse", get_reg_value(HKCU, r"Control Panel\Mouse", "MouseSpeed", "1") == "0")
        self.add_setting("Sticky", get_reg_value(HKCU, r"Control Panel\Accessibility\StickyKeys", "Flags", "510") == "506")

        # --- Action Buttons ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(pady=10, fill="x")

        self.btn_taskbar = ctk.CTkButton(self.action_frame, text=TRANSLATIONS[self.lang]["btn_taskbar"], fg_color="#374151", hover_color="#1F2937", font=ctk.CTkFont(weight="bold"), command=self.clear_taskbar)
        self.btn_taskbar.pack(side="left", padx=10, expand=True)

        self.btn_cleanup = ctk.CTkButton(self.action_frame, text=TRANSLATIONS[self.lang]["btn_cleanup"], fg_color="#374151", hover_color="#1F2937", font=ctk.CTkFont(weight="bold"), command=self.system_cleanup)
        self.btn_cleanup.pack(side="right", padx=10, expand=True)

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(pady=5, fill="x")

        self.btn_apply = ctk.CTkButton(self.bottom_frame, text=TRANSLATIONS[self.lang]["btn_apply"], fg_color="#10B981", hover_color="#059669", font=font_title, height=40, command=self.apply_changes)
        self.btn_apply.pack(side="left", padx=10, expand=True)

        self.btn_restore = ctk.CTkButton(self.bottom_frame, text=TRANSLATIONS[self.lang]["btn_restore"], fg_color="#EF4444", hover_color="#DC2626", font=font_title, height=40, command=self.restore_defaults)
        self.btn_restore.pack(side="right", padx=10, expand=True)

        self.btn_restart = ctk.CTkButton(self, text=TRANSLATIONS[self.lang]["btn_restart"], fg_color="#F59E0B", hover_color="#D97706", font=ctk.CTkFont(weight="bold", size=16), height=35, command=self.restart_explorer)
        self.btn_restart.pack(pady=(5,15), padx=30, fill="x")

    def create_section_title(self, text, color="#9CA3AF"):
        lbl = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color=color)
        lbl.pack(anchor="w", pady=(15, 5))
        return lbl
        
    def add_power_setting(self):
        row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=10)
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        t_data = TRANSLATIONS[self.lang]["settings"]["Power"]
        self.lbl_power_title = ctk.CTkLabel(info_frame, text=t_data["title"], font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        self.lbl_power_title.pack(anchor="w")
        self.lbl_power_desc = ctk.CTkLabel(info_frame, text=t_data["desc"], font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#6B7280")
        self.lbl_power_desc.pack(anchor="w")

        self.power_seg = ctk.CTkSegmentedButton(row, values=["Balanced", "High", "Ultimate"], variable=self.power_var, selected_color="#10B981", unselected_color="#374151")
        self.power_seg.pack(side="right")

    def add_setting(self, key, is_optimized):
        row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=10)
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        t_data = TRANSLATIONS[self.lang]["settings"][key]
        title_lbl = ctk.CTkLabel(info_frame, text=t_data["title"], font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        title_lbl.pack(anchor="w")
        desc_lbl = ctk.CTkLabel(info_frame, text=t_data["desc"], font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#6B7280")
        desc_lbl.pack(anchor="w")

        var = ctk.BooleanVar(value=is_optimized)
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
        el["status"].configure(text=t["on"] if state else t["off"])
        el["status"].configure(text_color="#10B981" if state else "#EF4444")

    def toggle_language(self):
        self.lang = "ar" if self.lang == "en" else "en"
        t = TRANSLATIONS[self.lang]
        
        self.btn_lang.configure(text=t["lang_btn"])
        self.title_label.configure(text=t["title"])
        self.subtitle.configure(text=t["subtitle"])
        
        self.lbl_perf.configure(text=t["cat_perf"])
        self.lbl_priv.configure(text=t["cat_priv"])
        self.lbl_ui.configure(text=t["cat_ui"])
        
        self.lbl_power_title.configure(text=t["settings"]["Power"]["title"])
        self.lbl_power_desc.configure(text=t["settings"]["Power"]["desc"])
        
        self.btn_taskbar.configure(text=t["btn_taskbar"])
        self.btn_cleanup.configure(text=t["btn_cleanup"])
        self.btn_apply.configure(text=t["btn_apply"])
        self.btn_restore.configure(text=t["btn_restore"])
        self.btn_restart.configure(text=t["btn_restart"])
        
        for key, el in self.ui_elements.items():
            st = t["settings"][key]
            el["title"].configure(text=st["title"])
            el["desc"].configure(text=st["desc"])
            self.refresh_status_label(key)

    def apply_changes(self):
        def run_cmds(cmds):
            for cmd in cmds: os.system(cmd + " >nul 2>&1")

        p = self.power_var.get()
        if p == "High":
            os.system('powershell -Command "$s=powercfg /l|?{$_ -match \'8c5e7fda\'};if(!$s){$n=powercfg -duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c;$g=$n -replace \'.*([0-9a-f\-]{36}).*\',\'$1\';powercfg /setactive $g}else{$g=$s[0] -replace \'.*([0-9a-f\-]{36}).*\',\'$1\';powercfg /setactive $g}" >nul 2>&1')
        elif p == "Ultimate":
            os.system('powershell -Command "$s=powercfg /l|?{$_ -match \'e9a42b02\'};if(!$s){$n=powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61;$g=$n -replace \'.*([0-9a-f\-]{36}).*\',\'$1\';powercfg /setactive $g}else{$g=$s[0] -replace \'.*([0-9a-f\-]{36}).*\',\'$1\';powercfg /setactive $g}" >nul 2>&1')
        else:
            os.system('powershell -Command "$s=powercfg /l|?{$_ -match \'381b4222\'};if(!$s){$n=powercfg -duplicatescheme 381b4222-f694-41f0-9685-ff5bb260df2e;$g=$n -replace \'.*([0-9a-f\-]{36}).*\',\'$1\';powercfg /setactive $g}else{$g=$s[0] -replace \'.*([0-9a-f\-]{36}).*\',\'$1\';powercfg /setactive $g}" >nul 2>&1')

        HKCU = "HKCU\\"
        HKLM = "HKLM\\"

        cmds = []
        if self.settings["BackApps"].get():
            cmds.extend([f'reg add "{HKCU}Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" /v GlobalUserDisabled /t REG_DWORD /d 1 /f', f'reg add "{HKLM}SYSTEM\\CurrentControlSet\\Services\\embeddedmode" /v Start /t REG_DWORD /d 4 /f'])
        else:
            cmds.extend([f'reg add "{HKCU}Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" /v GlobalUserDisabled /t REG_DWORD /d 0 /f', f'reg add "{HKLM}SYSTEM\\CurrentControlSet\\Services\\embeddedmode" /v Start /t REG_DWORD /d 3 /f'])

        if self.settings["DelOpt"].get():
            cmds.extend([f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization" /v DODownloadMode /t REG_DWORD /d 0 /f', 'sc config DoSvc start= disabled', 'net stop DoSvc'])
        else:
            cmds.extend([f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization" /v DODownloadMode /f', 'sc config DoSvc start= demand', 'net start DoSvc'])

        if self.settings["Edge"].get():
            cmds.extend([f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Edge" /v StartupBoostEnabled /t REG_DWORD /d 0 /f', f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Edge" /v BackgroundModeEnabled /t REG_DWORD /d 0 /f'])
        else:
            cmds.extend([f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Edge" /v StartupBoostEnabled /f', f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Edge" /v BackgroundModeEnabled /f'])

        if self.settings["Tele"].get():
            cmds.extend(['sc config DiagTrack start= disabled', 'sc stop DiagTrack', f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f'])
        else:
            cmds.extend(['sc config DiagTrack start= auto', 'sc start DiagTrack', f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /f'])

        if self.settings["Copilot"].get():
            cmds.extend([f'reg add "{HKCU}SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v TurnOffWindowsCopilot /t REG_DWORD /d 1 /f'])
        else:
            cmds.extend([f'reg delete "{HKCU}SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v TurnOffWindowsCopilot /f'])

        if self.settings["UAC"].get():
            cmds.extend([f'reg add "{HKLM}SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 0 /f'])
        else:
            cmds.extend([f'reg add "{HKLM}SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 5 /f'])

        if self.settings["Mouse"].get():
            cmds.extend([f'reg add "{HKCU}Control Panel\\Mouse" /v MouseSpeed /t REG_SZ /d 0 /f', f'reg add "{HKCU}Control Panel\\Mouse" /v MouseThreshold1 /t REG_SZ /d 0 /f', 'powershell -NoProfile -Command "$code=\'using System.Runtime.InteropServices; public class W32 { [DllImport(\\"user32.dll\\")] public static extern bool SystemParametersInfo(uint a, uint b, int[] c, uint d); }\'; Add-Type -TypeDefinition $code; $p=[int[]]@(0,0,0); [W32]::SystemParametersInfo(4,0,$p,3)"'])
        else:
            cmds.extend([f'reg add "{HKCU}Control Panel\\Mouse" /v MouseSpeed /t REG_SZ /d 1 /f', f'reg add "{HKCU}Control Panel\\Mouse" /v MouseThreshold1 /t REG_SZ /d 6 /f', 'powershell -NoProfile -Command "$code=\'using System.Runtime.InteropServices; public class W32 { [DllImport(\\"user32.dll\\")] public static extern bool SystemParametersInfo(uint a, uint b, int[] c, uint d); }\'; Add-Type -TypeDefinition $code; $p=[int[]]@(6,10,1); [W32]::SystemParametersInfo(4,0,$p,3)"'])

        if self.settings["MenuDelay"].get(): cmds.append(f'reg add "{HKCU}Control Panel\\Desktop" /v MenuShowDelay /t REG_SZ /d 20 /f')
        else: cmds.append(f'reg add "{HKCU}Control Panel\\Desktop" /v MenuShowDelay /t REG_SZ /d 400 /f')

        if self.settings["WallComp"].get(): cmds.append(f'reg add "{HKCU}Control Panel\\Desktop" /v JPEGImportQuality /t REG_DWORD /d 100 /f')
        else: cmds.append(f'reg delete "{HKCU}Control Panel\\Desktop" /v JPEGImportQuality /f')

        if self.settings["RecSec"].get(): cmds.append(f'reg add "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" /v HideRecommendedSection /t REG_DWORD /d 1 /f')
        else: cmds.append(f'reg delete "{HKLM}SOFTWARE\\Policies\\Microsoft\\Windows\\Explorer" /v HideRecommendedSection /f')

        if self.settings["Hiber"].get(): cmds.append('powercfg /h off')
        else: cmds.append('powercfg /h on')

        if self.settings["FastBoot"].get(): cmds.append(f'reg add "{HKLM}SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v HiberbootEnabled /t REG_DWORD /d 0 /f')
        else: cmds.append(f'reg add "{HKLM}SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v HiberbootEnabled /t REG_DWORD /d 1 /f')

        if self.settings["Sticky"].get(): cmds.append(f'reg add "{HKCU}Control Panel\\Accessibility\\StickyKeys" /v Flags /t REG_SZ /d 506 /f')
        else: cmds.append(f'reg add "{HKCU}Control Panel\\Accessibility\\StickyKeys" /v Flags /t REG_SZ /d 510 /f')

        threading.Thread(target=run_cmds, args=(cmds,), daemon=True).start()

        self.btn_apply.configure(text=TRANSLATIONS[self.lang]["applied_msg"], fg_color="#047857")
        self.after(2000, lambda: self.btn_apply.configure(text=TRANSLATIONS[self.lang]["btn_apply"], fg_color="#10B981"))

    def restore_defaults(self):
        self.power_var.set("Balanced")
        for key, var in self.settings.items(): var.set(False)
        self.apply_changes()

    def clear_taskbar(self):
        os.system(r'reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband" /v Favorites /f >nul 2>&1')
        os.system(r'reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband" /v FavoritesResolve /f >nul 2>&1')
        self.restart_explorer()

    def system_cleanup(self):
        def run_cleanup():
            self.btn_cleanup.configure(text="Cleaning...", state="disabled")
            cmds = [
                'del /f /s /q "%temp%\\*"', 'for /d %x in ("%temp%\\*") do rd /s /q "%x"',
                'del /f /s /q "%windir%\\Temp\\*"', 'for /d %x in ("%windir%\\Temp\\*") do rd /s /q "%x"',
                'del /f /s /q "%windir%\\Prefetch\\*"',
                'net stop wuauserv', 'net stop bits',
                'del /f /s /q "%windir%\\SoftwareDistribution\\Download\\*"',
                'net start wuauserv', 'net start bits',
                'powershell -NoProfile -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"',
                'for /F "tokens=*" %1 in (\'wevtutil.exe el\') do wevtutil.exe cl "%1"'
            ]
            for c in cmds: os.system(c + " >nul 2>&1")
            self.btn_cleanup.configure(text="Cleaned!", state="normal", fg_color="#047857")
            self.after(2000, lambda: self.btn_cleanup.configure(text=TRANSLATIONS[self.lang]["btn_cleanup"], fg_color="#374151"))
        threading.Thread(target=run_cleanup, daemon=True).start()

    def restart_explorer(self):
        os.system("taskkill /f /im explorer.exe >nul 2>&1")
        os.system("start explorer.exe")

if __name__ == "__main__":
    try:
        app = SystemTweakerApp()
        app.mainloop()
    except Exception as e:
        input(f"Error occurred: {e}\nPress Enter to close...")
