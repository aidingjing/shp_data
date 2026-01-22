"""测试字段编码"""
from src.core.exporter import ResultExporter

exporter = ResultExporter()

# 测试字段（来自用户的实际数据）
test_fields = ['实施年', '建设', '项目', '名称', '类型']

print("字段编码测试：")
print("=" * 50)
for field in test_fields:
    encoded = exporter._encode_field_name(field, prefix='t_')
    print(f"{field:12} -> {encoded:12} (长度: {len(encoded)})")

print("\n" + "=" * 50)
print("\n注意事项：")
print("- Shapefile 字段名最长 10 字符")
print("- 只支持 ASCII 字符")
print("- 编码后的字段名必须 <= 10 字符")
