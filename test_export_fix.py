"""测试字段编码修复"""
from src.core.exporter import ResultExporter

exporter = ResultExporter()

# 测试字段
print("测试字段编码:")
test_fields = ['实施年', '建设单位', 'project_name', 'id', 'name']
for field in test_fields:
    encoded = exporter._encode_field_name(field)
    print(f"  {field:12} -> {encoded}")

print("\n修复已完成！请按以下步骤操作：")
print("1. 完全关闭程序窗口")
print("2. 运行清理命令")
print("3. 重新运行程序: python main.py")
