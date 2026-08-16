"""
client_gui.py — Cliente de chat con interfaz gráfica (tkinter).

Características:
  - Ventana de chat con colores por usuario.
  - Panel lateral con usuarios conectados.
  - Indicador "está escribiendo..." en tiempo real.
  - Historial de mensajes al conectarse.
  - Mensajes privados: /privado @usuario mensaje
  - Comando /usuarios para refrescar la lista.
"""

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from protocol import decode, msg_mensaje, msg_escribiendo

HOST = "127.0.0.1"
PORT = 5000
BUFFER = 4096

# ── Paleta de colores ─────────────────────────────────────────────────────────
COLORES_USUARIO = [
    "#2196F3", "#E91E63", "#4CAF50", "#FF9800",
    "#9C27B0", "#00BCD4", "#F44336", "#009688",
]
COLOR_SISTEMA  = "#888888"
COLOR_PRIVADO  = "#FF6F00"
COLOR_BG       = "#1E1E2E"
COLOR_INPUT    = "#2A2A3E"
COLOR_TEXT     = "#CDD6F4"
COLOR_PANEL    = "#181825"
COLOR_TITULO   = "#CBA6F7"
COLOR_ESCRIBIENDO = "#A6ADC8"

TYPING_TIMEOUT = 2000  # ms sin escribir para cancelar el indicador


class ChatApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Chat Distribuido")
        self.root.configure(bg=COLOR_BG)
        self.root.geometry("900x600")
        self.root.minsize(700, 450)

        self.usuario = ""
        self.sock: socket.socket | None = None
        self.colores_map: dict[str, str] = {}
        self.color_idx = 0
        self.typing_timer = None
        self.enviando_typing = False

        self._construir_ui()
        self._conectar()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        # Título
        header = tk.Frame(self.root, bg=COLOR_PANEL, pady=8)
        header.pack(fill=tk.X)
        tk.Label(
            header, text="💬 Chat Distribuido",
            bg=COLOR_PANEL, fg=COLOR_TITULO,
            font=("Segoe UI", 14, "bold")
        ).pack(side=tk.LEFT, padx=16)
        self.lbl_estado = tk.Label(
            header, text="Conectando...",
            bg=COLOR_PANEL, fg=COLOR_SISTEMA,
            font=("Segoe UI", 10)
        )
        self.lbl_estado.pack(side=tk.RIGHT, padx=16)

        # Cuerpo principal
        cuerpo = tk.Frame(self.root, bg=COLOR_BG)
        cuerpo.pack(fill=tk.BOTH, expand=True)

        # Panel de chat (izquierda)
        panel_chat = tk.Frame(cuerpo, bg=COLOR_BG)
        panel_chat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.area_chat = scrolledtext.ScrolledText(
            panel_chat,
            state=tk.DISABLED,
            wrap=tk.WORD,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            padx=12, pady=8,
            insertbackground=COLOR_TEXT,
        )
        self.area_chat.pack(fill=tk.BOTH, expand=True, padx=(8, 0), pady=(8, 0))

        # Configurar tags de color
        self.area_chat.tag_config("sistema",  foreground=COLOR_SISTEMA,  font=("Segoe UI", 10, "italic"))
        self.area_chat.tag_config("privado",  foreground=COLOR_PRIVADO,  font=("Segoe UI", 11, "bold"))
        self.area_chat.tag_config("historial",foreground="#666680",       font=("Segoe UI", 10, "italic"))
        self.area_chat.tag_config("ts",       foreground="#585B70",       font=("Segoe UI", 9))
        self.area_chat.tag_config("yo",       foreground="#A6E3A1",       font=("Segoe UI", 11, "bold"))

        # Indicador "escribiendo"
        self.lbl_escribiendo = tk.Label(
            panel_chat, text="",
            bg=COLOR_BG, fg=COLOR_ESCRIBIENDO,
            font=("Segoe UI", 9, "italic"),
            anchor="w"
        )
        self.lbl_escribiendo.pack(fill=tk.X, padx=12)

        # Input
        frame_input = tk.Frame(panel_chat, bg=COLOR_INPUT, pady=6)
        frame_input.pack(fill=tk.X, padx=8, pady=8)

        self.entrada = tk.Entry(
            frame_input,
            bg=COLOR_INPUT, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            bd=0,
        )
        self.entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(12, 8), ipady=6)
        self.entrada.bind("<Return>", self._enviar)
        self.entrada.bind("<KeyRelease>", self._on_tecla)

        tk.Button(
            frame_input, text="Enviar",
            command=self._enviar,
            bg=COLOR_TITULO, fg=COLOR_PANEL,
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT, padx=16, pady=4,
            activebackground="#B4BEFE",
            cursor="hand2",
        ).pack(side=tk.RIGHT, padx=(0, 8))

        # Panel lateral de usuarios
        panel_usuarios = tk.Frame(cuerpo, bg=COLOR_PANEL, width=180)
        panel_usuarios.pack(side=tk.RIGHT, fill=tk.Y, padx=(4, 8), pady=8)
        panel_usuarios.pack_propagate(False)

        tk.Label(
            panel_usuarios, text="En línea",
            bg=COLOR_PANEL, fg=COLOR_TITULO,
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(12, 6))

        self.lista_usuarios = tk.Text(
            panel_usuarios,
            bg=COLOR_PANEL, fg=COLOR_TEXT,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            state=tk.DISABLED,
            cursor="arrow",
        )
        self.lista_usuarios.tag_config("verde", foreground="#A6E3A1")
        self.lista_usuarios.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

    # ── Conexión ──────────────────────────────────────────────────────────────

    def _conectar(self):
        usuario = simpledialog.askstring(
            "Nombre de usuario",
            "¿Con qué nombre querés entrar al chat?",
            parent=self.root
        )
        if not usuario or not usuario.strip():
            self.root.destroy()
            return
        self.usuario = usuario.strip()
        self.root.title(f"Chat Distribuido — {self.usuario}")

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
        except ConnectionRefusedError:
            messagebox.showerror("Error", f"No se pudo conectar al servidor {HOST}:{PORT}")
            self.root.destroy()
            return

        # Presentarse
        from protocol import msg_mensaje
        self.sock.sendall(msg_mensaje(self.usuario, ""))

        self.lbl_estado.config(text=f"Conectado como {self.usuario}")
        self.entrada.focus()

        # Hilo receptor
        threading.Thread(target=self._recibir, daemon=True).start()

    # ── Recepción ─────────────────────────────────────────────────────────────

    def _recibir(self):
        buffer_acum = ""
        while True:
            try:
                chunk = self.sock.recv(BUFFER).decode("utf-8")
                if not chunk:
                    break
                buffer_acum += chunk
                # Procesar líneas completas
                while "\n" in buffer_acum:
                    linea, buffer_acum = buffer_acum.split("\n", 1)
                    if linea.strip():
                        import json
                        try:
                            msg = json.loads(linea)
                            self.root.after(0, self._procesar_msg, msg)
                        except json.JSONDecodeError:
                            pass
            except Exception:
                break
        self.root.after(0, self._desconectado)

    def _procesar_msg(self, msg: dict):
        tipo = msg.get("tipo")

        if tipo == "mensaje":
            self._agregar_mensaje(msg)

        elif tipo == "sistema":
            self._agregar_sistema(msg.get("mensaje", ""), msg.get("timestamp", ""))

        elif tipo == "historial":
            self._agregar_sistema("── Historial de mensajes ──", "")
            for m in msg.get("mensajes", []):
                self._agregar_mensaje(m, es_historial=True)
            self._agregar_sistema("── Fin del historial ──", "")

        elif tipo == "usuarios":
            lista = msg.get("lista", [])
            self.lista_usuarios.delete(0, tk.END)
            self.lista_usuarios.config(state=tk.NORMAL)
            self.lista_usuarios.delete("1.0", tk.END)
            for u in lista:
                self.lista_usuarios.insert(tk.END, "● ", "verde")
                self.lista_usuarios.insert(tk.END, f"{u}\n")
            self.lista_usuarios.config(state=tk.DISABLED)

        elif tipo == "escribiendo":
            quien = msg.get("usuario", "")
            if quien != self.usuario:
                self.lbl_escribiendo.config(text=f"{quien} está escribiendo...")
                self.root.after(3000, lambda: self.lbl_escribiendo.config(text=""))

        elif tipo == "privado":
            de = msg.get("de", "")
            para = msg.get("para", "")
            texto = msg.get("mensaje", "")
            ts = msg.get("timestamp", "")
            if de == self.usuario:
                linea = f"[{ts}] 🔒 Tú → {para}: {texto}\n"
            else:
                linea = f"[{ts}] 🔒 {de} → ti: {texto}\n"
            self._escribir(linea, "privado")

    def _agregar_mensaje(self, msg: dict, es_historial: bool = False):
        usuario = msg.get("usuario", "?")
        texto   = msg.get("mensaje", "")
        ts      = msg.get("timestamp", "")

        if not texto:
            return

        tag_usuario = self._tag_usuario(usuario)
        tag_linea   = "historial" if es_historial else None

        self._escribir(f"[{ts}] ", "ts")
        if usuario == self.usuario:
            self._escribir(f"{usuario}: ", "yo")
        else:
            self._escribir(f"{usuario}: ", tag_usuario)
        self._escribir(f"{texto}\n", tag_linea)

    def _agregar_sistema(self, texto: str, ts: str):
        prefijo = f"[{ts}] " if ts else ""
        self._escribir(f"{prefijo}⚙ {texto}\n", "sistema")

    def _escribir(self, texto: str, tag: str | None = None):
        self.area_chat.config(state=tk.NORMAL)
        if tag:
            self.area_chat.insert(tk.END, texto, tag)
        else:
            self.area_chat.insert(tk.END, texto)
        self.area_chat.config(state=tk.DISABLED)
        self.area_chat.see(tk.END)

    def _tag_usuario(self, usuario: str) -> str:
        if usuario not in self.colores_map:
            color = COLORES_USUARIO[self.color_idx % len(COLORES_USUARIO)]
            self.colores_map[usuario] = color
            self.color_idx += 1
            self.area_chat.tag_config(f"u_{usuario}", foreground=color, font=("Segoe UI", 11, "bold"))
        return f"u_{usuario}"

    # ── Envío ─────────────────────────────────────────────────────────────────

    def _enviar(self, event=None):
        texto = self.entrada.get().strip()
        if not texto or not self.sock:
            return
        self.entrada.delete(0, tk.END)
        self.enviando_typing = False

        try:
            self.sock.sendall(msg_mensaje(self.usuario, texto))
        except Exception:
            self._desconectado()
            return

        # Mostrar el propio mensaje localmente
        if not texto.startswith("/"):
            from datetime import datetime
            ts = datetime.now().strftime("%H:%M:%S")
            self._escribir(f"[{ts}] ", "ts")
            self._escribir(f"{self.usuario}: ", "yo")
            self._escribir(f"{texto}\n")

    def _on_tecla(self, event=None):
        """Envía indicador de "escribiendo" con throttle."""
        if not self.sock:
            return
        texto = self.entrada.get().strip()
        if not texto:
            return
        if not self.enviando_typing:
            self.enviando_typing = True
            try:
                self.sock.sendall(msg_escribiendo(self.usuario))
            except Exception:
                pass
        if self.typing_timer:
            self.root.after_cancel(self.typing_timer)
        self.typing_timer = self.root.after(TYPING_TIMEOUT, self._reset_typing)

    def _reset_typing(self):
        self.enviando_typing = False

    # ── Desconexión ───────────────────────────────────────────────────────────

    def _desconectado(self):
        self.lbl_estado.config(text="Desconectado", fg="#F38BA8")
        self._agregar_sistema("Conexión perdida con el servidor.", "")
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None


def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
