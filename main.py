from datetime import datetime
import json
import math
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "water_tracker_pro.json"


class WaterTrackerProApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Control de Agua Pro - Joan")
    self.root.geometry("380x640")
    self.root.config(bg="#000000")
    self.root.resizable(False, False)

    self.load_data()
    self.wave_offset = 0

    # Contenedor principal estilo tarjeta moderna
    self.card = tk.Frame(
        root, bg="#0d0d0d", highlightbackground="#26060c", highlightthickness=2
    )
    self.card.place(x=20, y=20, width=340, height=600)

    # Títulos
    tk.Label(
        self.card,
        text="CONTROL DE AGUA",
        font=("Helvetica", 18, "bold"),
        bg="#0d0d0d",
        fg="#b91c3c",
    ).pack(pady=(25, 5))
    tk.Label(
        self.card,
        text="Diseño Exclusivo - Joan",
        font=("Helvetica", 10),
        bg="#0d0d0d",
        fg="#666666",
    ).pack(pady=(0, 15))

    # Lienzo para el pote y las ondas de agua animadas
    self.canvas = tk.Canvas(
        self.card, width=130, height=210, bg="#121212", highlightthickness=0
    )
    self.canvas.pack(pady=10)

    # Etiqueta de mensajes de estado
    self.msg_label = tk.Label(
        self.card,
        text="",
        font=("Helvetica", 13, "bold"),
        bg="#0d0d0d",
        fg="#cc2936",
    ),
    self.msg_label = tk.Label(
        self.card,
        text="¡Comienza a hidratarte hoy!",
        font=("Helvetica", 13, "bold"),
        bg="#0d0d0d",
        fg="#cc2936",
    )
    self.msg_label.pack(pady=15)

    # Botón principal estilizado
    self.btn_drink = tk.Button(
        self.card,
        text="💧 ¡Ya bebí!",
        font=("Helvetica", 14, "bold"),
        bg="#58111A",
        fg="white",
        activebackground="#b91c3c",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=self.drink_water,
    )
    self.btn_drink.pack(ipadx=20, ipady=8, pady=10)

    # Iniciar bucle de animación de ondas constante
    self.animate_waves()
    self.update_ui_state()

  def load_data(self):
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(DATA_FILE):
      try:
        with open(DATA_FILE, "r") as f:
          data = json.load(f)
          if data.get("date") == today:
            self.count = data.get("count", 0)
            return
      except:
        pass
    self.count = 0
    self.save_data()

  def save_data(self):
    today = datetime.now().strftime("%Y-%m-%d")
    data = {"date": today, "count": self.count}
    with open(DATA_FILE, "w") as f:
      json.dump(data, f)

  def play_sound_effect(self, tipo):
    # Genera alertas de audio nativas en Windows/Linux sin archivos externos
    try:
      import winsound

      if tipo == "click":
        winsound.Beep(700, 80)
      elif tipo == "goal":
        winsound.Beep(523, 150)
        winsound.Beep(659, 150)
        winsound.Beep(784, 250)
    except:
      pass  # Si no soporta winsound en el equipo, continúa sin error

  def drink_water(self):
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(DATA_FILE):
      with open(DATA_FILE, "r") as f:
        data = json.load(f)
        if data.get("date") != today:
          self.count = 0

    if self.count < 6:
      self.count += 1
      self.save_data()
      self.play_sound_effect("click")

      if self.count == 4 or self.count == 6:
        self.play_sound_effect("goal")

      self.update_ui_state()
    else:
      self.play_sound_effect("click")
      messagebox.showinfo(
          "Meta cumplida",
          "¡Ya has alcanzado el máximo de potes registrados para hoy!",
      )

  def update_ui_state(self):
    if self.count == 4:
      self.msg_label.config(text="¡Muy bien, Joan!", fg="#ff4d6d")
    elif self.count >= 6:
      self.msg_label.config(text="¡Excelente, Joan!", fg="#ff1a3c")
    elif self.count > 0:
      self.msg_label.config(
          text=f"¡Buen ritmo! Potes tomados: {self.count}", fg="#e5989b"
      )
    else:
      self.msg_label.config(text="¡Comienza a hidratarte hoy!", fg="#8c8c8c")

  def animate_waves(self):
    # Actualiza el movimiento de las ondas y dibuja el pote en tiempo real
    self.wave_offset += 0.15
    self.draw_pot_with_waves()
    self.root.after(50, self.animate_waves)

  def draw_pot_with_waves(self):
    self.canvas.delete("all")

    # 1. Tapa del pote
    self.canvas.create_rectangle(
        45, 10, 85, 22, fill="#222222", outline="#444444", width=2
    )
    # Cuello
    self.canvas.create_line(45, 22, 35, 40, width=2, fill="#444444")
    self.canvas.create_line(85, 22, 95, 40, width=2, fill="#444444")

    # 2. Cuerpo del pote de vidrio oscuro
    self.canvas.create_rectangle(
        35, 40, 95, 190, outline="#444444", width=3, fill="#181818"
    )

    # 3. Cálculo de altura del agua según el conteo (máximo 6)
    max_height = 145
    fill_ratio = self.count / 6.0
    water_height = fill_ratio * max_height
    surface_y = 185 - water_height

    # 4. Dibujar el agua con efecto de onda matemática si hay contenido
    if self.count > 0:
      points = [36, 189]  # Esquina inferior izquierda

      # Generar puntos de la onda senoidal en la superficie
      for x in range(36, 95, 3):
        y = surface_y + math.sin(x * 0.1 + self.wave_offset) * 3
        points.append(x)
        points.append(y)

      points.extend([94, 189])  # Esquina inferior derecha
      self.canvas.create_polygon(points, fill="#881337", outline="")
      # Brillo superior de la onda
      self.canvas.create_line(
          36, surface_y, 94, surface_y, fill="#ff1a3c", width=2
      )

    # Líneas divisorias de medida en el pote
    for i in range(1, 6):
      y_line = 40 + (i * max_height / 6)
      self.canvas.create_line(
          35, y_line, 95, y_line, fill="#2c2c2c", dash=(2, 2)
      )

    # Texto central con el contador
    self.canvas.create_text(
        65, 115, text=f"{self.count}/6", font=("Helvetica", 16, "bold"), fill="white"
    )


if __name__ == "__main__":
  root = tk.Tk()
  app = WaterTrackerProApp(root)
  root.mainloop()