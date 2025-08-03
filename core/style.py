class Style:
    BG = "#2E3440"
    WIDGET_BG = "#3B4252"
    TEXT = "#FBFBFB"
    PRIMARY = "#88C0D0"
    ACCENT = "#5E81AC"
    ERROR = "#BF616A"
    SUCCESS = '#8FBCBB'
    
    TEXT_DARK = "#2E3440"
    TAB_INACTIVE_BG = "#D8DEE9"

    FONT = "Segoe UI"
    FONT_BOLD = "Segoe UI Bold"
    ENTRY = {"font": (FONT, 12), "bg": WIDGET_BG, "fg": TEXT, "relief": "solid", "borderwidth": 1, "highlightthickness": 1, "highlightbackground": ACCENT, "highlightcolor": PRIMARY, "insertbackground": TEXT}
    BUTTON = {"font": (FONT_BOLD, 12), "bg": ACCENT, "fg": TEXT, "activebackground": PRIMARY, "activeforeground": BG, "relief": "raised", "borderwidth": 2, "padx": 10, "pady": 5}
    LABEL = {"bg": BG, "fg": TEXT, "font": (FONT_BOLD, 12)}