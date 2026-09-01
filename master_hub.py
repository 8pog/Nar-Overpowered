import customtkinter as ctk
import os
import subprocess

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# قاموس الترجمة (عربي / إنجليزي)
TRANSLATIONS = {
    "en": {
        "title": "NAR UTILITIES HUB",
        "subtitle": "All-in-One System Optimization",
        "dev": "By Developer Nar",
        "lang_btn": "عربي",
        "ready": "Ready.",
        "tools": {
            "explorer_config": "Explorer Configuration",
            "system_tweaker": "System Tweaker",
            "bloatware_remover": "Bloatware Remover",
            "ai_manager": "Windows AI Manager"
        },
        "launched": "Launched",
        "not_found": "Error: {0} not found!"
    },
    "ar": {
        "title": "NAR UTILITIES HUB",
        "subtitle": "تحسين شامل لنظام التشغيل",
        "dev": "By Developer Nar",
        "lang_btn": "English",
        "ready": "جاهز.",
        "tools": {
            "explorer_config": "إعدادات المستكشف",
            "system_tweaker": "مُحسّن النظام",
            "bloatware_remover": "مزيل التطبيقات المزعجة",
            "ai_manager": "مدير الذكاء الاصطناعي"
        },
        "launched": "تم تشغيل",
        "not_found": "خطأ: لم يتم العثور على {0}!"
    }
}

class MasterHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lang = "en"
        self.tool_buttons = {}

        self.title("Nar Utilities Hub - Developer Nar")
        self.geometry("500x600")
        self.resizable(False, False)

        font_title = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        font_sub = ctk.CTkFont(family="Segoe UI", size=14)
        font_dev = ctk.CTkFont(family="Segoe UI", size=12)

        # الإطار العلوي للعنوان وزر اللغة
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(15, 5), padx=20)
        self.header_frame.columnconfigure(0, weight=1)
        self.header_frame.columnconfigure(1, weight=1)
        self.header_frame.columnconfigure(2, weight=1)

        # زر تبديل اللغة في الزاوية اليمنى
        self.btn_lang = ctk.CTkButton(
            self.header_frame, 
            text=TRANSLATIONS[self.lang]["lang_btn"], 
            width=60, 
            height=30, 
            fg_color="#374151", 
            hover_color="#1F2937", 
            command=self.toggle_language
        )
        self.btn_lang.grid(row=0, column=2, sticky="ne")

        # العناوين الرئيسية
        self.title_label = ctk.CTkLabel(self, text=TRANSLATIONS[self.lang]["title"], font=font_title, text_color="#00FFFF")
        self.title_label.pack(pady=(10, 5))
        
        self.subtitle = ctk.CTkLabel(self, text=TRANSLATIONS[self.lang]["subtitle"], font=font_sub, text_color="#FACC15")
        self.subtitle.pack(pady=(0, 2))

        self.dev_label = ctk.CTkLabel(self, text=TRANSLATIONS[self.lang]["dev"], font=font_dev, text_color="#9CA3AF")
        self.dev_label.pack(pady=(0, 20))

        # حاوية الأزرار
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(fill="both", expand=True, padx=40)

        # إنشاء الأزرار للأدوات الأربعة
        self.create_tool_button("explorer_config", "#10B981")
        self.create_tool_button("system_tweaker", "#3B82F6")
        self.create_tool_button("bloatware_remover", "#EF4444")
        self.create_tool_button("ai_manager", "#8B5CF6")

        # رسالة تنبيه أسفل الشاشة
        self.status_lbl = ctk.CTkLabel(self, text=TRANSLATIONS[self.lang]["ready"], font=ctk.CTkFont(size=12), text_color="#9CA3AF")
        self.status_lbl.pack(pady=15)

    def create_tool_button(self, file_name, hover_color):
        t = TRANSLATIONS[self.lang]["tools"]
        btn = ctk.CTkButton(
            self.buttons_frame, 
            text=t[file_name], 
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            height=45,
            fg_color="#374151",
            hover_color=hover_color,
            command=lambda: self.launch_tool(file_name)
        )
        btn.pack(fill="x", pady=8)
        self.tool_buttons[file_name] = btn

    def toggle_language(self):
        self.lang = "ar" if self.lang == "en" else "en"
        t = TRANSLATIONS[self.lang]
        
        self.btn_lang.configure(text=t["lang_btn"])
        self.title_label.configure(text=t["title"])
        self.subtitle.configure(text=t["subtitle"])
        self.dev_label.configure(text=t["dev"])
        self.status_lbl.configure(text=t["ready"])

        for key, btn in self.tool_buttons.items():
            btn.configure(text=t["tools"][key])

    def launch_tool(self, file_name):
        t = TRANSLATIONS[self.lang]
        if os.path.exists(f"{file_name}.exe"):
            subprocess.Popen(f"{file_name}.exe")
            self.status_lbl.configure(text=f"{t['launched']} {file_name}.exe", text_color="#10B981")
        elif os.path.exists(f"{file_name}.py"):
            subprocess.Popen(["python", f"{file_name}.py"])
            self.status_lbl.configure(text=f"{t['launched']} {file_name}.py", text_color="#10B981")
        else:
            self.status_lbl.configure(text=t["not_found"].format(file_name), text_color="#EF4444")

if __name__ == "__main__":
    app = MasterHubApp()
    app.mainloop()
