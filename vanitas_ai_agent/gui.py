"""Simple Tkinter GUI for vanitas_ai_agent."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, scrolledtext

from vanitas_ai_agent.agent import VanitasAgent
from vanitas_ai_agent.config import Settings


class AgentGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("vanitas_ai_agent GUI")
        self.root.geometry("820x560")

        try:
            settings = Settings.from_env()
            self.agent = VanitasAgent(settings)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("配置错误", f"初始化 Agent 失败: {exc}")
            self.agent = None

        self._build_widgets()

    def _build_widgets(self) -> None:
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(top_frame, text="输入指令:").pack(side=tk.LEFT)
        self.entry = tk.Entry(top_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.entry.bind("<Return>", lambda _event: self.on_send())

        send_btn = tk.Button(top_frame, text="发送", command=self.on_send)
        send_btn.pack(side=tk.LEFT)

        self.output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.output.insert(tk.END, "欢迎使用 vanitas_ai_agent 图形界面。\n")

    def on_send(self) -> None:
        if not self.agent:
            messagebox.showwarning("不可用", "Agent 未正确初始化，请检查 OPENAI_API_KEY。")
            return

        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.output.insert(tk.END, f"\nYou> {user_text}\n")
        self.entry.delete(0, tk.END)
        self.root.update_idletasks()

        try:
            result = self.agent.process(user_text)
        except Exception as exc:  # noqa: BLE001
            result = f"[ERROR] {exc}"

        self.output.insert(tk.END, f"Agent> {result}\n")
        self.output.see(tk.END)


def launch_gui() -> None:
    root = tk.Tk()
    AgentGUI(root)
    root.mainloop()
