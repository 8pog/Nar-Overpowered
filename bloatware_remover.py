import customtkinter as ctk
import os
import subprocess
import ctypes
import sys
import threading

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

TRANSLATIONS = {
    "en": {
        "title": "BLOATWARE REMOVER",
        "subtitle": "By Developer Nar",
        "btn_remove_all": "Remove All Bloatware",
        "status_loading": "Scanning installed apps...",
        "status_done": "Scan Complete!",
        "lang_btn": "عربي",
        "apps": {
            "Cam": "Windows Camera", "Dev": "Dev Home", "Hub": "Feedback Hub",
            "Copilot": "Microsoft 365 Copilot", "Bing": "Microsoft Bing Search",
            "Clip": "Microsoft Clipchamp", "News": "Microsoft News",
            "Teams": "Microsoft Teams", "ToDo": "Microsoft To Do",
            "Outlook": "Outlook for Windows", "Power": "Power Automate",
            "Quick": "Quick Assist", "Sol": "Microsoft Solitaire",
            "Sound": "Sound Recorder", "Sticky": "Sticky Notes"
        }
    },
    "ar": {
        "title": "مزيل التطبيقات المزعجة",
        "subtitle": "By Developer Nar",
        "btn_remove_all": "حذف جميع التطبيقات",
        "status_loading": "جاري فحص التطبيقات المثبتة...",
        "status_done": "اكتمل الفحص!",
        "lang_btn": "English",
        "apps": {
            "Cam": "الكاميرا (Camera)", "Dev": "بيئة التطوير (Dev Home)", "Hub": "مركز الملاحظات",
            "Copilot": "مساعد الذكاء الاصطناعي (Copilot)", "Bing": "بحث بنج (Bing Search)",
            "Clip": "محرر الفيديو (Clipchamp)", "News": "الأخبار (Microsoft News)",
            "Teams": "مايكروسوفت تيمز (Teams)", "ToDo": "المهام (To Do)",
            "Outlook": "البريد (Outlook)", "Power": "التشغيل الآلي (Power Automate)",
            "Quick": "المساعدة السريعة (Quick Assist)", "Sol": "لعبة السوليتير (Solitaire)",
            "Sound": "مسجل الصوت (Sound Recorder)", "Sticky": "الملاحظات (Sticky Notes)"
        }
    }
}

APP_PACKAGES = {
    "Cam": "WindowsCamera", "Dev": "DevHome", "Hub": "WindowsFeedbackHub",
    "Copilot": "Copilot|Windows.Ai", "Bing": "BingSearch", "Clip": "Clipchamp",
    "News": "BingNews", "Teams": "MSTeams", "ToDo": "Todos",
    "Outlook": "OutlookForWindows", "Power": "PowerAutomateDesktop",
    "Quick": "QuickAssist", "Sol": "SolitaireCollection",
    "Sound": "WindowsSoundRecorder", "Sticky": "StickyNotes"
}

class BloatwareRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.lang = "en"
        self.ui_elements = {}
        self.app_status = {k: True for k in APP_PACKAGES.keys()}

        self.title("Bloatware Remover - Developer Nar")
        self.geometry("650x780")
        self.resizable(False, False)

        font_title = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        font_sub = ctk.CTkFont(family="Segoe UI", size=14)

        # Header Frame
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

        # Loading Status
        self.status_label = ctk.CTkLabel(self, text=TRANSLATIONS[self.lang]["status_loading"], font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color="#FACC15")
        self.status_label.pack(pady=5)

        # Main Scrollable Frame
        self.main_frame = ctk.CTkScrollableFrame(self, width=600, height=520, fg_color="transparent")
        self.main_frame.pack(padx=20, pady=5, fill="both", expand=True)

        for key in APP_PACKAGES.keys():
            self.create_app_row(key)

        # Bottom Frame
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(pady=15, fill="x")

        self.btn_remove_all = ctk.CTkButton(self.bottom_frame, text=TRANSLATIONS[self.lang]["btn_remove_all"], fg_color="#EF4444", hover_color="#DC2626", font=font_title, height=45, command=self.remove_all)
        self.btn_remove_all.pack(padx=30, fill="x")

        threading.Thread(target=self.scan_apps, daemon=True).start()

    def create_app_row(self, key):
        row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=10)

        name_lbl = ctk.CTkLabel(row, text=TRANSLATIONS[self.lang]["apps"][key], font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        name_lbl.pack(side="left")

        action_btn = ctk.CTkButton(row, text="Remove", width=80, fg_color="#374151", hover_color="#1F2937", font=ctk.CTkFont(weight="bold"), state="disabled", command=lambda k=key: self.remove_single(k))
        action_btn.pack(side="right", padx=(10, 0))

        status_lbl = ctk.CTkLabel(row, text="Scanning...", width=80, font=ctk.CTkFont(family="Segoe UI", weight="bold"), text_color="#9CA3AF")
        status_lbl.pack(side="right")

        self.ui_elements[key] = {"name": name_lbl, "status": status_lbl, "btn": action_btn}

    def scan_apps(self):
        try:
            out = subprocess.check_output('powershell -NoProfile -Command "Get-AppxPackage -AllUsers | Select-Object -ExpandProperty Name"', shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            for key, package_str in APP_PACKAGES.items():
                is_installed = False
                for pkg in package_str.split('|'):
                    if pkg.lower() in out.lower():
                        is_installed = True
                        break
                self.app_status[key] = is_installed
            
            if "Bing" in APP_PACKAGES:
                try:
                    subprocess.check_output('reg query "HKCU\\Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableSearchBoxSuggestions', shell=True, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
                    self.app_status["Bing"] = False 
                except:
                    self.app_status["Bing"] = True 

        except Exception as e:
            print("Scan error:", e)

        self.after(0, self.update_ui_after_scan)

    def update_ui_after_scan(self):
        self.status_label.configure(text=TRANSLATIONS[self.lang]["status_done"], text_color="#10B981")
        for key, elements in self.ui_elements.items():
            installed = self.app_status[key]
            if installed:
                elements["status"].configure(text="Installed" if self.lang=="en" else "مُثبت", text_color="#EF4444")
                elements["btn"].configure(state="normal", text="Remove" if self.lang=="en" else "إزالة")
            else:
                elements["status"].configure(text="Removed" if self.lang=="en" else "تمت الإزالة", text_color="#10B981")
                elements["btn"].configure(state="disabled", text="Done" if self.lang=="en" else "منظف")

    def toggle_language(self):
        self.lang = "ar" if self.lang == "en" else "en"
        t = TRANSLATIONS[self.lang]
        
        self.title_label.configure(text=t["title"])
        self.subtitle.configure(text=t["subtitle"])
        self.btn_lang.configure(text=t["lang_btn"])
        self.btn_remove_all.configure(text=t["btn_remove_all"])
        
        if self.status_label.cget("text") in [TRANSLATIONS["en"]["status_loading"], TRANSLATIONS["ar"]["status_loading"]]:
            self.status_label.configure(text=t["status_loading"])
        else:
            self.status_label.configure(text=t["status_done"])

        for key, el in self.ui_elements.items():
            el["name"].configure(text=t["apps"][key])
            if self.app_status[key]:
                el["status"].configure(text="Installed" if self.lang=="en" else "مُثبت")
                el["btn"].configure(text="Remove" if self.lang=="en" else "إزالة")
            else:
                el["status"].configure(text="Removed" if self.lang=="en" else "تمت الإزالة")
                el["btn"].configure(text="Done" if self.lang=="en" else "منظف")

    def execute_removal(self, package_name):
        cmd = f'powershell -NoProfile -Command "Get-AppxPackage -Name \'*{package_name}*\' -AllUsers | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue; $prov = Get-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue; if ($prov) {{ $prov | Where-Object {{ $_.DisplayName -like \'*{package_name}*\' }} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue }}"'
        subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

    def remove_single(self, key):
        self.ui_elements[key]["btn"].configure(state="disabled", text="Working...")
        
        def task():
            if key == "Copilot":
                os.system("taskkill /f /im msedgewebview2.exe >nul 2>&1")
                os.system("taskkill /f /im msedge.exe >nul 2>&1")
                os.system('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v "TurnOffWindowsCopilot" /t REG_DWORD /d 1 /f >nul 2>&1')
                os.system('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v "TurnOffWindowsCopilot" /t REG_DWORD /d 1 /f >nul 2>&1')
                os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowCopilotButton /t REG_DWORD /d 0 /f >nul 2>&1')
                os.system('winget uninstall --name "Microsoft 365 Copilot" --silent --accept-source-agreements >nul 2>&1')
                self.execute_removal("Copilot")
                self.execute_removal("Windows.Ai")
            elif key == "Bing":
                self.execute_removal("BingSearch")
                os.system('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableSearchBoxSuggestions /t REG_DWORD /d 1 /f >nul 2>&1')
            elif key == "Teams":
                os.system("taskkill /f /im msteams.exe >nul 2>&1")
                self.execute_removal(APP_PACKAGES[key])
            elif key == "ToDo":
                os.system("taskkill /f /im Todo.exe >nul 2>&1")
                self.execute_removal(APP_PACKAGES[key])
            elif key == "Outlook":
                os.system("taskkill /f /im olk.exe >nul 2>&1")
                self.execute_removal(APP_PACKAGES[key])
            elif key == "Power":
                os.system("taskkill /f /im PowerAutomate.exe >nul 2>&1")
                os.system("taskkill /f /im PAD.Console.Host.exe >nul 2>&1")
                self.execute_removal(APP_PACKAGES[key])
            else:
                self.execute_removal(APP_PACKAGES[key])

            self.app_status[key] = False
            self.after(0, self.update_ui_after_scan)

        threading.Thread(target=task, daemon=True).start()

    def remove_all(self):
        self.btn_remove_all.configure(state="disabled", text="Removing All... Please Wait", fg_color="#374151")
        for key, el in self.ui_elements.items():
            if self.app_status[key]:
                el["btn"].configure(state="disabled")
                el["status"].configure(text="Removing...", text_color="#FACC15")

        def task():
            processes = ["PowerAutomate.exe", "PAD.Console.Host.exe", "Todo.exe", "msteams.exe", "olk.exe", "msedgewebview2.exe", "msedge.exe"]
            for p in processes: os.system(f"taskkill /f /im {p} >nul 2>&1")

            os.system('winget uninstall --name "Microsoft 365 Copilot" --silent --accept-source-agreements >nul 2>&1')
            os.system('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v "TurnOffWindowsCopilot" /t REG_DWORD /d 1 /f >nul 2>&1')
            os.system('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v "TurnOffWindowsCopilot" /t REG_DWORD /d 1 /f >nul 2>&1')
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowCopilotButton /t REG_DWORD /d 0 /f >nul 2>&1')
            os.system('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableSearchBoxSuggestions /t REG_DWORD /d 1 /f >nul 2>&1')

            apps_to_remove = "WindowsCamera,DevHome,WindowsFeedbackHub,Clipchamp,BingNews,MSTeams,Todos,OutlookForWindows,PowerAutomateDesktop,QuickAssist,SolitaireCollection,WindowsSoundRecorder,StickyNotes,Copilot,Windows.Ai,BingSearch"
            cmd = f'powershell -NoProfile -Command "$apps = \'{apps_to_remove}\'.Split(\',\'); $prov = Get-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue; foreach($a in $apps){{ Get-AppxPackage -Name \\"*$a*\\" -AllUsers | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue; if ($prov) {{ $prov | Where-Object {{$_.DisplayName -like \\"*$a*\\"}} | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue }} }}"'
            subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

            for key in self.app_status.keys():
                self.app_status[key] = False

            self.after(0, self.update_ui_after_scan)
            self.after(0, lambda: self.btn_remove_all.configure(state="normal", text=TRANSLATIONS[self.lang]["btn_remove_all"], fg_color="#EF4444"))

        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    try:
        app = BloatwareRemoverApp()
        app.mainloop()
    except Exception as e:
        input(f"Error occurred: {e}\nPress Enter to close...")
