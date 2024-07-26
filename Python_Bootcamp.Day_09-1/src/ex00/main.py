import calculator

# Вызов функций
print(calculator.add(10.0, 21))  # 3510
print(calculator.sub(14, 21))  # -7
print(calculator.mul(14, 21))  # 294
print(calculator.div(15, 7.7))   # 2
try:
    print(calculator.div(15, 0))
except ZeroDivisionError as err:
    print(err)
