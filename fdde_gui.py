import tkinter as tk
from tkinter import messagebox


# 判断闰年
def isLeapYear(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# 校验八位表达式
def isValid8Digit(date8):
    if len(date8) != 8 or not date8.isdigit():
        return False
    year = int(date8[:4])
    month = int(date8[4:6])
    day = int(date8[6:8])

    if month < 1 or month > 12:
        return False

    # 校验日期
    if month in [1, 3, 5, 7, 8, 10, 12] and (day < 1 or day > 31):
        return False
    elif month in [4, 6, 9, 11] and (day < 1 or day > 30):
        return False
    elif month == 2:
        if isLeapYear(year) and (day < 1 or day > 29):
            return False
        elif not isLeapYear(year) and (day < 1 or day > 28):
            return False

    return True


# 校验铁定日期表达式
def isValidFDDE(dateFDDE):
    if len(dateFDDE) < 3:
        return False
    # 校验年月日格式
    try:
        year_expr = dateFDDE[:-3]
        month_expr = dateFDDE[-3]
        day_expr = dateFDDE[-2:]

        # 字符验证
        if not all(c.isupper() or c.isdigit() for c in year_expr):
            return False
        if not month_expr.isdigit() and not month_expr.isalpha():
            return False
        if not day_expr.isdigit():
            return False

        return True
    except:
        return False


# 8位表达式转换成铁定表达式
def convertToFDDE(year, month, day):
    year_expr = ""
    if year < 2022:
        year_expr = str(2022 - year)
    else:
        year_offset = year - 2022
        while year_offset >= 0:
            year_expr = chr(65 + (year_offset % 26)) + year_expr
            year_offset //= 26
    month_expr = str(month) if month <= 9 else chr(64 + (month - 10))
    day_expr = f"{day:02d}"

    return f"{year_expr}{month_expr}{day_expr}"


# 铁定表达式转换为8位表达式
def convertTo8Digit(year_expr, month_expr, day_expr):
    # 如果年份部分是数字，直接转换为年份
    if year_expr.isdigit():
        year = 2022 - int(year_expr)  # 使用 2022 - n 计算公元年份
    else:
        # 计算年份偏移
        year_offset = 0
        for i in range(len(year_expr) - 1, -1, -1):
            year_offset += (ord(year_expr[i]) - ord('A')) * (26 ** (len(year_expr) - 1 - i))

        # 注意，年份是基于 2022 年的偏移
        year = 2022 + year_offset

    # 处理月份：如果是字母，则转为对应的数字
    if month_expr.isdigit():
        month = int(month_expr)
    else:
        month = ord(month_expr) - 64 + 9  # 'A' -> 10, 'B' -> 11, 'C' -> 12

    day = int(day_expr)

    # 生成八位日期表达式
    result = f"{year:04d}{month:02d}{day:02d}"

    # 校验转换后的八位日期是否合法
    if not isValid8Digit(result):
        return None  # 返回 None 表示日期不合法

    return result


# 处理用户输入的转换
def handle_conversion():
    input_value = entry.get().strip()
    selected_option = conversion_option.get()

    if selected_option == "八位表达式 -> 铁定表达式":
        if isValid8Digit(input_value):
            year = int(input_value[:4])
            month = int(input_value[4:6])
            day = int(input_value[6:8])
            result = convertToFDDE(year, month, day)
            result_label.config(text=f"转换结果: {result}")
        else:
            messagebox.showerror("错误", "无效的八位日期表达式")
    elif selected_option == "铁定表达式 -> 八位表达式":
        if isValidFDDE(input_value):
            year_expr = input_value[:-3]
            month_expr = input_value[-3]
            day_expr = input_value[-2:]
            result = convertTo8Digit(year_expr, month_expr, day_expr)
            if result is None:
                messagebox.showerror("错误", "转换后的八位日期表达式不合法")
            else:
                result_label.config(text=f"转换结果: {result}")
        else:
            messagebox.showerror("错误", "无效的铁定日期表达式")
    else:
        messagebox.showerror("错误", "请选择转换方向")


# 创建 GUI
root = tk.Tk()
root.title("日期转换器")

# 输入框
entry_label = tk.Label(root, text="请输入日期（八位或铁定表达式）:")
entry_label.pack(pady=10)
entry = tk.Entry(root, width=20)
entry.pack(pady=5)

# 转换选项
conversion_option = tk.StringVar(value="八位表达式 -> 铁定表达式")
option_frame = tk.Frame(root)
tk.Radiobutton(option_frame, text="八位表达式 -> 铁定表达式", variable=conversion_option,
               value="八位表达式 -> 铁定表达式").pack(side=tk.LEFT)
tk.Radiobutton(option_frame, text="铁定表达式 -> 八位表达式", variable=conversion_option,
               value="铁定表达式 -> 八位表达式").pack(side=tk.LEFT)
option_frame.pack(pady=10)

# 转换按钮
convert_button = tk.Button(root, text="开始转换", command=handle_conversion)
convert_button.pack(pady=20)

# 显示结果的标签
result_label = tk.Label(root, text="转换结果:")
result_label.pack(pady=10)

# 启动 GUI
root.mainloop()
