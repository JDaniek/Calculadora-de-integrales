import tkinter as tk
from tkinter import Label, Button, Frame, Entry, Listbox
from core.style import Style

def create_calculator_tab(parent, app_instance):
    Label(parent, text="Función f(x):", **Style.LABEL).pack(anchor="w")
    vcmd = (app_instance.register(app_instance.logic._validate_entry), '%P')
    app_instance.func_entry = Entry(parent, **Style.ENTRY, validate="focusout", validatecommand=vcmd)
    app_instance.func_entry.pack(fill=tk.X, pady=(5, 15))
    
    Label(parent, text="Límite inferior (a):", **Style.LABEL).pack(anchor="w")
    app_instance.lower_limit_entry = Entry(parent, **Style.ENTRY, validate="focusout", validatecommand=vcmd)
    app_instance.lower_limit_entry.pack(fill=tk.X, pady=5)
    
    Label(parent, text="Límite superior (b):", **Style.LABEL).pack(anchor="w")
    app_instance.upper_limit_entry = Entry(parent, **Style.ENTRY, validate="focusout", validatecommand=vcmd)
    app_instance.upper_limit_entry.pack(fill=tk.X, pady=(5, 15))

    calc_frame = Frame(parent, bg=Style.BG)
    calc_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    create_calculator_buttons(calc_frame, app_instance)

def create_calculator_buttons(parent, app_instance):
    button_symbols = {'sqrt(': '√', 'pi': 'π', 'oo': '∞', 'exp(': 'eˣ', '^': 'xʸ', '*': '×', '/': '÷'}
    buttons = [
        ['sin(', 'cos(', 'tan(', 'ln(', 'log('], ['sqrt(', 'exp(', '^', '(', ')'],
        ['7', '8', '9', '/', '⌫'], ['4', '5', '6', '*', '-'],
        ['1', '2', '3', '+', '='], ['0', '.', 'x', 'pi', 'oo']
    ]
    for i in range(5): parent.columnconfigure(i, weight=1)
    for i, row in enumerate(buttons):
        for j, val in enumerate(row):
            style = Style.BUTTON.copy()
            display_text = button_symbols.get(val, val)
            if val == '⌫': cmd, style['bg'] = app_instance.logic.backspace, Style.ERROR
            elif val == '=': cmd, style['bg'] = app_instance.logic.calculate_integral, Style.SUCCESS
            else: cmd = lambda v=val: app_instance.logic.insert_text(v)
            Button(parent, text=display_text, command=cmd, **style).grid(row=i, column=j, padx=2, pady=2, sticky="nsew")

def create_history_tab(parent, app_instance):
    Label(parent, text="Historial de Operaciones:", **Style.LABEL).pack(anchor="w", pady=5)
    app_instance.history_listbox = Listbox(parent, bg=Style.WIDGET_BG, fg=Style.TEXT, font=(Style.FONT, 10), relief="solid", borderwidth=1)
    app_instance.history_listbox.pack(fill="both", expand=True)
    Button(parent, text="Limpiar Historial", command=app_instance.logic.clear_history, **Style.BUTTON).pack(pady=10)

def create_memory_tab(parent, app_instance):
    Label(parent, text="Memoria de Resultados (Definida):", **Style.LABEL).pack(anchor="w", pady=5)
    app_instance.memory_listbox = Listbox(parent, bg=Style.WIDGET_BG, fg=Style.TEXT, font=(Style.FONT, 10), relief="solid", borderwidth=1)
    app_instance.memory_listbox.pack(fill="both", expand=True)
    Button(parent, text="Limpiar Memoria", command=app_instance.logic.clear_memory, **Style.BUTTON).pack(pady=10)