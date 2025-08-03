import tkinter as tk
from tkinter import ttk, Label, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from core.style import Style
from src.calculator import IntegralCalculatorLogic
from core.widgets import create_calculator_tab, create_history_tab, create_memory_tab

# --- CLASE PRINCIPAL DE LA APLICACIÓN ---
class IntegralCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # --- Configuración de la ventana principal ---
        self.title("Calculadora de Integrales Avanzada")
        self.configure(bg=Style.BG)
        self.geometry("1200x750")
        self.minsize(1000, 600)

        # Instancia de la lógica
        self.logic = IntegralCalculatorLogic(self)

        # --- Variables de estado y memoria ---
        self.operation_history = []
        self.result_memory = []

        # --- Creación de la Interfaz ---
        self._create_menu()
        self._create_widgets()
        self._create_status_bar()
        self._bind_contextual_help()
        
        self.update_status("Listo. Ingrese una función para comenzar.")

    def _create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Exportar Historial a PDF", command=self.logic.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=self.logic.show_help_manual)
        help_menu.add_command(label="Acerca de...", command=self.logic.show_about_dialog)

    def _create_status_bar(self):
        self.status_bar = Label(self, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=Style.WIDGET_BG, fg=Style.TEXT)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message):
        self.status_bar.config(text=message)

    def _create_widgets(self):
        left_frame = Frame(self, bg=Style.BG, width=400, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)

        right_frame = Frame(self, bg=Style.BG, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        input_frame = Frame(left_frame, bg=Style.BG)
        input_frame.pack(pady=10, fill=tk.X)
        
        notebook = ttk.Notebook(input_frame)
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=(Style.FONT, 10), padding=[5, 2])
        style.configure("TNotebook", background=Style.BG, borderwidth=0)
        style.map("TNotebook.Tab", 
                  background=[("selected", Style.PRIMARY), ("!selected", Style.TAB_INACTIVE_BG)], 
                  foreground=[("selected", Style.TEXT_DARK), ("!selected", Style.TEXT_DARK)])
        notebook.pack(pady=10, fill="both", expand=True)

        calc_tab = Frame(notebook, bg=Style.BG)
        notebook.add(calc_tab, text='Calculadora')
        create_calculator_tab(calc_tab, self)

        history_tab = Frame(notebook, bg=Style.BG)
        notebook.add(history_tab, text='Historial')
        create_history_tab(history_tab, self)

        memory_tab = Frame(notebook, bg=Style.BG)
        notebook.add(memory_tab, text='Memoria')
        create_memory_tab(memory_tab, self)
        
        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.logic.clear_plot()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()
        
    def _bind_contextual_help(self):
        self.func_entry.bind("<Enter>", lambda e: self.update_status("Ingrese la función a integrar. Ejemplo: sin(x) o x**2"))
        self.func_entry.bind("<Leave>", lambda e: self.update_status("Listo"))
        self.lower_limit_entry.bind("<Enter>", lambda e: self.update_status("Límite inferior de integración. Puede ser un número o una expresión como 'pi/2' o '-oo'"))
        self.lower_limit_entry.bind("<Leave>", lambda e: self.update_status("Listo"))
        self.upper_limit_entry.bind("<Enter>", lambda e: self.update_status("Límite superior de integración. Puede ser un número o una expresión como 'pi' o 'oo'"))
        self.upper_limit_entry.bind("<Leave>", lambda e: self.update_status("Listo"))