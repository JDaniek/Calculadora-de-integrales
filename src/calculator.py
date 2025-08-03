import numpy as np
from sympy import symbols, sympify, lambdify, integrate, latex, pi, exp, sin, cos, tan, log, sqrt, oo
import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from core.style import Style

x = symbols('x')
math_dict = {
    'pi': pi, 'π': pi, 'e': exp(1), 'E': exp(1), 'exp': exp, 'sin': sin,
    'cos': cos, 'tan': tan, 'ln': log, 'log': log, 'sqrt': sqrt, 'oo': oo, '∞': oo, 'x': x
}

class IntegralCalculatorLogic:
    def __init__(self, app_instance):
        self.app = app_instance

    def _validate_entry(self, value_if_allowed):
        if not value_if_allowed:
            return True
        try:
            sympify(value_if_allowed, locals=math_dict)
            self.app.update_status("Entrada válida.")
            return True
        except (SyntaxError, TypeError):
            self.app.update_status(f"Expresión no válida: '{value_if_allowed}'")
            return False

    def calculate_integral(self):
        try:
            func_str = self.app.func_entry.get().strip().replace("^", "**")
            if not func_str:
                raise ValueError("La función no puede estar vacía.")
            
            a_str = self.app.lower_limit_entry.get().strip()
            if not a_str:
                raise ValueError("El límite inferior no puede estar vacío.")
            
            b_str = self.app.upper_limit_entry.get().strip()
            if not b_str:
                raise ValueError("El límite superior no puede estar vacío.")

            a = sympify(a_str, locals=math_dict)
            b = sympify(b_str, locals=math_dict)
            func = sympify(func_str, locals=math_dict)

            result_def = integrate(func, (x, a, b)).evalf()
            result_indef = integrate(func, x)

            history_entry = f"∫({func_str}) dx de {a_str} a {b_str} ≈ {result_def:.4f}"
            self.add_to_history(history_entry)
            self.add_to_memory(f"{result_def:.4f}")

            self.plot_function(func, a, b)
            self.app.canvas.draw()
            self.app.update_status("Cálculo completado exitosamente.")

        except (ValueError, SyntaxError) as e:
            messagebox.showerror("Error de Entrada", f"Por favor, revisa los campos de entrada.\n\nDetalle: {e}")
            self.app.update_status(f"Error de entrada: {e}")
        except Exception as e:
            messagebox.showerror("Error de Cálculo", f"No se pudo procesar la integral.\nAsegúrate de que la sintaxis es correcta (ej. 'x**2' en lugar de 'x2').\n\nError: {e}")
            self.app.update_status(f"Error de cálculo: {e}")

    def plot_function(self, func, a, b):
        self.app.ax.clear()
        self.app.ax.set_facecolor(Style.WIDGET_BG)
        self.app.fig.patch.set_facecolor(Style.BG)
        f = lambdify(x, func, modules=["numpy"])
        
        a_f, b_f = float(a) if a != -oo else -10, float(b) if b != oo else 10
        if a == -oo and b == oo: a_f, b_f = -10, 10
        elif a == -oo: a_f = b_f - 20
        elif b == oo: b_f = a_f + 20
        
        x_vals_plot = np.linspace(a_f - 2, b_f + 2, 1000)
        y_vals_plot = f(x_vals_plot)
        x_vals_fill = np.linspace(a_f, b_f, 500)
        y_vals_fill = f(x_vals_fill)

        self.app.ax.plot(x_vals_plot, y_vals_plot, label=f"f(x) = ${latex(func)}$", color=Style.PRIMARY)
        self.app.ax.fill_between(x_vals_fill, y_vals_fill, color=Style.PRIMARY, alpha=0.4, label="Área de la integral")
        self.app.ax.axhline(0, color=Style.TEXT, linewidth=0.7)
        self.app.ax.axvline(0, color=Style.TEXT, linewidth=0.7)
        self.app.ax.grid(True, linestyle="--", alpha=0.2, color=Style.TEXT)
        self.app.ax.tick_params(axis='x', colors=Style.TEXT)
        self.app.ax.tick_params(axis='y', colors=Style.TEXT)
        for spine in self.app.ax.spines.values():
            spine.set_edgecolor(Style.TEXT)
        legend = self.app.ax.legend(facecolor=Style.BG, edgecolor=Style.ACCENT)
        for text in legend.get_texts():
            text.set_color(Style.TEXT)
        self.app.ax.set_title("Gráfica de la Función", color=Style.TEXT, fontname=Style.FONT, fontsize=14)
        self.app.ax.set_xlabel("x", color=Style.TEXT)
        self.app.ax.set_ylabel("f(x)", color=Style.TEXT)
        
    def add_to_history(self, entry):
        self.app.operation_history.append(entry)
        self.app.history_listbox.insert(tk.END, entry)

    def add_to_memory(self, result):
        self.app.result_memory.append(result)
        self.app.memory_listbox.insert(tk.END, result)
        
    def clear_history(self):
        self.app.operation_history.clear()
        self.app.history_listbox.delete(0, tk.END)
        self.app.update_status("Historial limpiado.")

    def clear_memory(self):
        self.app.result_memory.clear()
        self.app.memory_listbox.delete(0, tk.END)
        self.app.update_status("Memoria limpiada.")

    def clear_plot(self):
        self.app.ax.clear()
        self.app.ax.set_facecolor(Style.WIDGET_BG)
        self.app.fig.patch.set_facecolor(Style.BG)
        self.app.ax.grid(True, linestyle="--", alpha=0.2, color=Style.TEXT)
        self.app.ax.axhline(0, color=Style.TEXT, linewidth=0.7)
        self.app.ax.axvline(0, color=Style.TEXT, linewidth=0.7)
        self.app.ax.tick_params(axis='x', colors=Style.TEXT)
        self.app.ax.tick_params(axis='y', colors=Style.TEXT)
        for spine in self.app.ax.spines.values():
            spine.set_edgecolor(Style.TEXT)
        self.app.ax.set_title("Gráfica de la Función", color=Style.TEXT, fontname=Style.FONT, fontsize=14)
        if hasattr(self.app, 'canvas'):
            self.app.canvas.draw()
        
    def insert_text(self, value):
        self.app.func_entry.insert(tk.INSERT, value)
        self.app.func_entry.focus()

    def backspace(self):
        current_text = self.app.func_entry.get()
        if current_text:
            self.app.func_entry.delete(len(current_text) - 1, tk.END)

    def export_to_pdf(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if filename:
            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica", 12)
            y_position = letter[1] - inch
            for entry in self.app.operation_history:
                c.drawString(inch, y_position, entry)
                y_position -= 20
                if y_position < inch:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = letter[1] - inch
            c.save()
            messagebox.showinfo("Exportar a PDF", "Historial exportado a PDF exitosamente.")

    def show_help_manual(self):
        messagebox.showinfo("Manual de Usuario", "Esta es una calculadora de integrales avanzada. Para usarla, ingrese la función y los límites de integración y presione '='. Puede usar las teclas de los botones para ingresar funciones comunes. Los límites pueden ser números, 'pi' o 'oo' (infinito).")

    def show_about_dialog(self):
        messagebox.showinfo("Acerca de...", "Calculadora de Integrales Avanzada\n\nCreada con Python, Tkinter, SymPy y Matplotlib.\nVersión 1.0\n\nEste software es de código abierto y tiene como objetivo ayudar en el cálculo de integrales.")