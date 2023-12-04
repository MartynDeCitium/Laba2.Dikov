import streamlit as st
import matplotlib.pyplot as plt
import random
from PIL import Image

# Устанавливаем конфигурацию страницы
st.set_page_config(page_title="Исследование преобразователя частоты", page_icon=":chart_with_upwards_trend:")

st.sidebar.title("Лабораторная работа №4")
st.sidebar.subheader("Исследование преобразователя частоты")

# Главная страница
if st.sidebar.radio("Выберите тип измерения", ["Исследование предельной характеристики", "Исследование нагрузочной характеристики"]) == "Исследование предельной характеристики":
    # Ваш код для главной страницы
    st.title("Исследование предельной характеристики")


    # Проверяем, было ли уже сгенерировано рандомное число в текущей сессии
    if 'random_number' not in st.session_state:
        # Если нет, генерируем новое рандомное число и сохраняем в глобальной переменной
        st.session_state.random_number = random.uniform(-1, 1)

    # Инициализируем массив в сессионном состоянии
    if 'data_array' not in st.session_state:
        st.session_state.data_array = []
    st.image("ПЧ.jpg", caption="Рисунок 1. Схема лабораторной установки", use_column_width=True)
    # Ввод значения напряжения переменного тока
    Uinput = st.number_input('Введите Входное напряжение преобразователя', min_value=100, max_value=220, value=220, step=1)
    st.write('Uвх ПЧ-50/25 = ', Uinput, ' В')
    Uvih = round(0.083*Uinput+16.74, 2)  # Пересчет выходного напряжения ПЧ

    # Добавляем слайдер с сопротивлением нагрузки
    RLoad = st.slider("Сопротивление нагрузки", 6.50, 25.00, 8.50)
    Rvn = 0.5

    ILoad = round(Uvih/(RLoad+Rvn), 2)
    Usr = 24*ILoad + 86 + st.session_state.random_number
    # st.write("Напряжение срыва", Usr, 'В')
    if Uinput < Usr:
        st.error('Срыв колебаний ПЧ')
        st.write("Ток нагрузки", I0, 'А')
        st.write("Напряжение на нагрузке", U0, 'В')
    else:
        st.write("Ток нагрузки", ILoad, 'А')
        st.write("Напряжение на нагрузке", Uvih, 'В')

    # Обработчик событий для слайдера
    if st.button("Добавить в массив"):
        # Добавляем кортеж в массив
        st.session_state.data_array.append((ILoad, Uinput))
        st.success(f"Добавлено в массив: ({ILoad}, {Uinput})")

    # Выводим все значения массива Вариант 2
    st.write("Значения массива:", ", ".join([f"({x}, {y})" for x, y in st.session_state.data_array]))

    # Построение графика
    if st.button("Построить график"):
        # Извлекаем значения из массива для построения графика
        x_values = [item[0] for item in st.session_state.data_array]
        y_values = [item[1] for item in st.session_state.data_array]

        # Строим график
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, marker='o')
        ax.set_ylabel('Напряжение на нагрузке')
        ax.set_xlabel('Ток нагрузки')
        ax.set_title('Нагрузочная характеристика')
        # Добавляем сетку
        ax.grid(True)
        # Отображаем график
        st.pyplot(fig)

# Другая страница
else:
    st.title("Исследование нагрузочной характеристики")
    st.image("ПЧ.jpg", caption="Рисунок 1. Схема лабораторной установки", use_column_width=True)
    # Ваш код для другой страницы
    # Генерируем новое рандомное число и сохраняем в переменной
    random_number = random.uniform(-0.1, 0.1)

    # Выводим рандомное число
    # st.write(f'Ваше рандомизированное число: {random_number}')

    # Инициализируем массив в сессионном состоянии
    if 'data_array' not in st.session_state:
        st.session_state.data_array = []

    # Ввод значения напряжения переменного тока
    Uinput = st.number_input('Введите Входное напряжение преобразователя', min_value=160, max_value=220, value="min", step=1)
    st.write('Uвх ПЧ-50/25 = ', Uinput, ' В')
    U0 = 0.083*Uinput+16.74  # Пересчет выходного напряжения ПЧ
    # st.write('Uвых ПЧ-50/25 = ', U0, ' В')
    U01 = U0 + random_number
    # st.write('Uвых R ПЧ-50/25 = ', U01, ' В')

    # Добавляем слайдер с сопротивлением нагрузки
    RLoad = st.slider("Сопротивление нагрузки", 6.50, 25.00, 8.50)
    Rvn = 0.5

    ILoad1 = U01/(RLoad+Rvn)
    Udiod = 0.2*ILoad1+0.1
    ULoad1 = RLoad*ILoad1-Udiod
    ILoad = round(ILoad1, 2)
    ULoad = round(ULoad1, 2)
    # st.write("Напряжение диода", Udiod, 'В')
    st.write("Ток нагрузки", ILoad, 'А')
    st.write("Напряжение на нагрузке", ULoad, 'В')

    # Обработчик событий для слайдера
    if st.button("Добавить в массив"):
        # Добавляем кортеж в массив
        st.session_state.data_array.append((ILoad, ULoad))
        st.success(f"Добавлено в массив: ({ILoad}, {ULoad})")

    # Выводим все значения массива Вариант 2
    st.write("Значения массива:", ", ".join([f"({x}, {y})" for x, y in st.session_state.data_array]))

    # Построение графика
    if st.button("Построить график"):
        # Извлекаем значения из массива для построения графика
        x_values = [item[0] for item in st.session_state.data_array]
        y_values = [item[1] for item in st.session_state.data_array]

        # Строим график
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, marker='o')
        ax.set_ylabel('Напряжение на нагрузке')
        ax.set_xlabel('Ток нагрузки')
        ax.set_title('Нагрузочная характеристика')
        # Добавляем сетку
        ax.grid(True)
        # Отображаем график
        st.pyplot(fig)
