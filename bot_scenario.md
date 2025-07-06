# Сценарий работы Telegram-бота

## 1. Начало диалога
- Пользователь запускает бота командой `/start`
- Бот приветствует и предлагает выбрать действие:
  ```text
  "Добрый день! Я помогу записаться к врачу. Выберите:"
  1. 📅 Записаться на прием
  2. 🕒 Проверить мои записи
  

## 2. Опишите ваши симптомы или выберите специализацию:
- /therapist - Терапевт
- /cardiologist - Кардиолог
- /dentist - Стоматолог

## 3. Выбор врача и времени
Бот показывает доступных врачей:
Доступные специалисты:
1. Иванова А.П. (Кардиолог) ★★★★☆
2. Петров В.С. (Кардиолог) ★★★★★

Свободное время у Петрова В.С.:
- 🕘 20 июля 10:00-10:30
- 🕚 20 июля 11:00-11:30

## 4. Подтверждение записи
Бот создает запись через API:

POST /appointments
Body: {
  "patient_name": "Иван Петров",
  "doctor_id": 2,
  "start_time": "2025-07-20T10:00:00"
}

"✅ Вы записаны к Петрову В.С. на 20 июля в 10:00"



---

## 5. stub-реализацию (опционально)**

```python
from typing import Optional
from pydantic import BaseModel
import requests

class SymptomAnalysis(BaseModel):
    speciality: str  # Определенная специализация
    confidence: float  # Достоверность (0.0-1.0)

class Bot:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def analyze_symptoms(self, text: str) -> SymptomAnalysis:
        """Заглушка для ИИ-анализа симптомов"""
        return SymptomAnalysis(speciality="cardiologist", confidence=0.85)

    def create_appointment(self, user_id: int, time_slot: str) -> Optional[str]:
        """Заглушка создания записи через API"""
        response = requests.post(
            f"{self.api_url}/appointments",
            json={
                "patient_name": f"User_{user_id}",
                "doctor_id": 1,
                "start_time": time_slot
            }
        )
        return response.json().get("id") if response.ok else None

# Пример использования
if __name__ == "__main__":
    bot = Bot(api_url="http://localhost:8000")
    analysis = bot.analyze_symptoms("Болит сердце")
    print(f"Рекомендуемый специалист: {analysis.speciality}")