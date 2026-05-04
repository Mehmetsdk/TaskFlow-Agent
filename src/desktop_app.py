from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from src.agent import TaskAgent


class ChatDesktopApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("AI Chat")
        self.root.geometry("860x640")
        self.root.minsize(720, 520)

        self.agent = self._create_agent()
        self.response_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.processing = False

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.after(120, self._poll_queue)

    def _create_agent(self) -> TaskAgent:
        try:
            return TaskAgent()
        except Exception as exc:
            messagebox.showerror("Startup error", f"Could not start the agent:\n{exc}")
            raise

    def _build_ui(self) -> None:
        self.root.configure(bg="#f4f6f8")

        container = ttk.Frame(self.root, padding=18)
        container.pack(fill="both", expand=True)

        title = ttk.Label(container, text="AI Chat", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w", pady=(0, 12))

        subtitle = ttk.Label(
            container,
            text="Press Enter to send. Use Shift+Enter for a new line.",
            wraplength=760,
        )
        subtitle.pack(anchor="w", pady=(0, 10))

        self.chat_area = scrolledtext.ScrolledText(
            container,
            wrap="word",
            height=24,
            font=("Segoe UI", 11),
            state="disabled",
            padx=14,
            pady=14,
            background="#fbfcfe",
            relief="solid",
            borderwidth=1,
        )
        self.chat_area.pack(fill="both", expand=True, pady=(0, 12))
        self.chat_area.tag_configure(
            "user",
            background="#dff1ff",
            foreground="#0f172a",
            justify="right",
            lmargin1=120,
            lmargin2=120,
            rmargin=16,
            spacing1=8,
            spacing3=8,
        )
        self.chat_area.tag_configure(
            "agent",
            background="#eef2f7",
            foreground="#0f172a",
            justify="left",
            lmargin1=16,
            lmargin2=16,
            rmargin=120,
            spacing1=8,
            spacing3=8,
        )
        self.chat_area.tag_configure(
            "system",
            background="#fff7d6",
            foreground="#4b5563",
            justify="left",
            lmargin1=16,
            lmargin2=16,
            rmargin=120,
            spacing1=6,
            spacing3=6,
        )
        self.chat_area.tag_configure(
            "error",
            background="#ffe4e6",
            foreground="#9f1239",
            justify="left",
            lmargin1=16,
            lmargin2=16,
            rmargin=120,
            spacing1=6,
            spacing3=6,
        )
        self.chat_area.tag_configure("sender", font=("Segoe UI", 10, "bold"))

        input_frame = ttk.Frame(container)
        input_frame.pack(fill="x")

        self.input_text = tk.Text(input_frame, height=4, font=("Segoe UI", 11), wrap="word")
        self.input_text.pack(side="left", fill="x", expand=True)
        self.input_text.bind("<Return>", self._send_from_shortcut)
        self.input_text.bind("<Shift-Return>", self._insert_newline)
        self.input_text.bind("<Control-Return>", self._send_from_shortcut)

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(side="right", padx=(12, 0), fill="y")

        self.send_button = ttk.Button(button_frame, text="Send", command=self.send_message)
        self.send_button.pack(fill="x", pady=(0, 8))

        clear_button = ttk.Button(button_frame, text="Clear", command=self._clear_chat)
        clear_button.pack(fill="x")

        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(container, textvariable=self.status_var, anchor="w")
        status_bar.pack(fill="x", pady=(10, 0))

        self._append_system_message("Ready. Ask a question or request a task to begin.")

    def _send_from_shortcut(self, event: tk.Event) -> str:
        self.send_message()
        return "break"

    def _insert_newline(self, event: tk.Event) -> str:
        self.input_text.insert(tk.INSERT, "\n")
        return "break"

    def _clear_chat(self) -> None:
        self._set_chat_text("")
        self._append_system_message("Chat cleared.")

    def _set_chat_text(self, text: str) -> None:
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", tk.END)
        if text:
            self.chat_area.insert(tk.END, text)
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)

    def _append_message(self, sender: str, content: str, tag: str) -> None:
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, f"{sender}:\n", ("sender", tag))
        self.chat_area.insert(tk.END, f"{content}\n\n", tag)
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)

    def _append_system_message(self, content: str) -> None:
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, f"System:\n{content}\n\n", ("sender", "system"))
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)

    def _set_busy(self, busy: bool) -> None:
        self.processing = busy
        self.send_button.configure(state="disabled" if busy else "normal")
        self.input_text.configure(state="disabled" if busy else "normal")
        self.status_var.set("Thinking..." if busy else "Ready")

    def send_message(self) -> None:
        if self.processing:
            return

        prompt = self.input_text.get("1.0", tk.END).strip()
        if not prompt:
            return

        self.input_text.delete("1.0", tk.END)
        self._append_message("You", prompt, "user")
        self._set_busy(True)

        worker = threading.Thread(target=self._generate_reply, args=(prompt,), daemon=True)
        worker.start()

    def _generate_reply(self, prompt: str) -> None:
        try:
            reply = self.agent.process_input(prompt)
            self.response_queue.put(("ok", reply))
        except Exception as exc:
            self.response_queue.put(("error", str(exc)))

    def _poll_queue(self) -> None:
        try:
            status, payload = self.response_queue.get_nowait()
        except queue.Empty:
            self.root.after(120, self._poll_queue)
            return

        if status == "ok":
            self._append_message("Agent", payload, "agent")
        else:
            self._append_message("Agent", f"Error: {payload}", "error")

        self._set_busy(False)
        self.root.after(120, self._poll_queue)

    def _on_close(self) -> None:
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def launch_app() -> None:
    try:
        app = ChatDesktopApp()
    except Exception:
        return

    app.run()
