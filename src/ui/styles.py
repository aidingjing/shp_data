"""
UI 样式定义模块
提供 PyQt5 样式表
"""

from ..utils.constants import COLORS, FONTS, SPACING


def get_stylesheet(theme='light') -> str:
    """
    获取应用样式表

    Args:
        theme: 主题 ('light' 或 'dark')

    Returns:
        CSS 样式表字符串
    """
    if theme == 'dark':
        colors = {
            'background': COLORS['dark_background'],
            'surface': COLORS['dark_surface'],
            'border': COLORS['dark_border'],
            'text_primary': COLORS['dark_text_primary'],
            'text_secondary': COLORS['dark_text_secondary'],
        }
    else:
        colors = {
            'background': COLORS['background'],
            'surface': COLORS['surface'],
            'border': COLORS['border'],
            'text_primary': COLORS['text_primary'],
            'text_secondary': COLORS['text_secondary'],
        }

    stylesheet = f"""
    QMainWindow {{
        background-color: {colors['background']};
        color: {colors['text_primary']};
    }}

    QGroupBox {{
        font-size: 13px;
        font-weight: 600;
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
        border-radius: 6px;
        margin-top: 12px;
        padding: 12px;
        background-color: {colors['surface']};
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        padding: 0 6px;
        background-color: {colors['surface']};
    }}

    QPushButton {{
        background-color: {COLORS['primary']};
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: {SPACING['padding_button']};
        font-size: {FONTS['body']}px;
        font-weight: 500;
        min-width: 80px;
    }}

    QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}

    QPushButton:pressed {{
        background-color: {COLORS['primary_dark']};
        padding: 9px 15px 7px 17px;
    }}

    QPushButton:disabled {{
        background-color: {colors['border']};
        color: {COLORS['text_disabled']};
    }}

    QLineEdit, QTextEdit {{
        background-color: {colors['background']};
        color: {colors['text_primary']};
        border: 1px solid {colors['border']};
        border-radius: 4px;
        padding: {SPACING['padding_input']};
        font-size: {FONTS['body']}px;
    }}

    QLineEdit:focus, QTextEdit:focus {{
        border: 2px solid {COLORS['primary']};
        padding: 5px 11px;
    }}

    QCheckBox {{
        spacing: 8px;
        font-size: {FONTS['body']}px;
        color: {colors['text_primary']};
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {colors['border']};
        border-radius: 3px;
        background-color: {colors['background']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {COLORS['primary']};
        border: 2px solid {COLORS['primary']};
    }}

    QProgressBar {{
        border: 1px solid {colors['border']};
        border-radius: 4px;
        background-color: {COLORS['surface_variant']};
        text-align: center;
        color: {colors['text_primary']};
        font-size: 12px;
        font-weight: 600;
    }}

    QProgressBar::chunk {{
        background-color: {COLORS['primary']};
        border-radius: 3px;
    }}

    QTextEdit[log="true"] {{
        font-family: {FONTS['mono']};
        font-size: {FONTS['mono']}px;
        line-height: 1.5;
        background-color: {COLORS['dark_surface']};
        color: {COLORS['dark_text_primary']};
    }}
    """

    return stylesheet
