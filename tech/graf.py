import json
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

DATA_FILE = "json/temp.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка при загрузке данных из JSON: {e}")
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def plot_temperature(temperature_data, date_format='%d.%m.%Y %H:%M'):
    if not temperature_data or len(temperature_data) == 0:
        return None

    times = []
    temperatures = []
    for item in temperature_data:
        try:
            parts = item.split(maxsplit=1)
            if len(parts) != 2:
                raise ValueError(f"Неверный формат данных: {item}")
            temp, time_str = parts
            temperature = float(temp)
            time_obj = datetime.strptime(time_str, date_format)
            times.append(time_obj)
            temperatures.append(temperature)
        except (ValueError, TypeError) as e:
            print(f"Ошибка при обработке данных в plot_temperature: {e}, данные: {item}")
            return None

    if not times or not temperatures or len(times) != len(temperatures):
        print("Ошибка: Невозможно построить график из-за несоответствия данных.")
        return None

    plt.plot(times, temperatures, marker='o', linestyle='-')
    plt.xlabel("Время")
    plt.ylabel("Температура (°C)")
    plt.title("График температуры тела")
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(date_format))
    plt.tight_layout()

    buf = BytesIO()
    try:
        plt.savefig(buf, format='png')
    except Exception as e:
        print(f"Ошибка при сохранении графика: {e}")
        return None

    buf.seek(0)
    plt.close()
    return buf
