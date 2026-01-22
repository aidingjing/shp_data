"""
常量定义模块
包含颜色、间距、字体、配置等常量
"""

# 颜色方案
COLORS = {
    # 主色调
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_light': '#BBDEFB',

    # 功能色
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'info': '#2196F3',

    # 地图图层颜色
    'source_layer': '#2196F3',
    'target_layer': 'rgba(255, 152, 0, 0.3)',
    'joined': '#4CAF50',
    'unjoined': '#F44336',
    'highlight': '#FFEB3B',

    # 中性色（浅色主题）
    'background': '#FFFFFF',
    'surface': '#F5F5F5',
    'surface_variant': '#EEEEEE',
    'border': '#BDBDBD',
    'text_primary': '#212121',
    'text_secondary': '#757575',
    'text_disabled': '#9E9E9E',

    # 中性色（深色主题）
    'dark_background': '#1E1E1E',
    'dark_surface': '#2D2D2D',
    'dark_surface_variant': '#3D3D3D',
    'dark_border': '#555555',
    'dark_text_primary': '#E0E0E0',
    'dark_text_secondary': '#A0A0A0',
}

# 字体规范
FONTS = {
    'default': '"Segoe UI", "Microsoft YaHei UI", sans-serif',
    'mono': '"Consolas", "Monaco", "Courier New", monospace',
    'h1': 24,
    'h2': 18,
    'h3': 15,
    'body': 13,
    'small': 11,
    'mono': 12,
}

# 间距系统（8px 网格）
SPACING = {
    'unit': 8,
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    'padding_button': '8px 16px',
    'padding_input': '6px 12px',
    'padding_group': '12px',
}

# 组件尺寸
SIZES = {
    'window_min_width': 900,
    'window_min_height': 650,
    'window_default_width': 1200,
    'window_default_height': 800,
    'button_height_medium': 36,
    'button_height_small': 32,
    'input_height': 32,
    'progress_height': 24,
}

# 日志级别
LOG_LEVELS = {
    'INFO': 'INFO',
    'SUCCESS': 'SUCCESS',
    'WARNING': 'WARNING',
    'ERROR': 'ERROR',
}

# 应用配置
APP_CONFIG = {
    'name': '空间关联分析工具',
    'version': '1.0.0',
    'author': 'GIS Team',
}
