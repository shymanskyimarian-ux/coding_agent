import os
import sys
import io
import google.generativeai as genai
from dotenv import load_dotenv

# --- 1. ІНІЦІАЛІЗАЦІЯ ТА ПЕРЕВІРКА БЕЗПЕКИ ---
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "your_api_key_here":
    print("\n" + "="*60)
    print("❌ КРИТИЧНА ПОМИЛКА: API-ключ не знайдено або він недійсний!")
    print("="*60)
    print("Інструкція з налаштування:")
    print("1. Знайдіть файл '.env.example' у цій папці.")
    print("2. Зробіть його копію та назвіть '.env' (з крапкою на початку).")
    print("3. Вставте ваш реальний ключ GEMINI_API_KEY у файл '.env'.")
    print("4. Запустіть скрипт знову.")
    print("="*60 + "\n")
    sys.exit(1)

genai.configure(api_key=api_key)

# --- 2. ІНСТРУМЕНТ: ПІСОЧНИЦЯ ВИКОНАННЯ КОДУ ---
def execute_python_code(code: str) -> str:
    """
    Виконує переданий Python код і повертає результат виводу (stdout) або текст помилки.
    Використовуй цей інструмент, щоб ТЕСТУВАТИ свій код.
    Завжди додавай print() у свій код, щоб побачити результат розрахунків.
    """
    print("\n[АГЕНТ ТЕСТУЄ КОД]:\n" + "-"*40)
    print(code)
    print("-" * 40)
    
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    
    try:
        exec(code, {}) # Порожній словник для безпечної ізоляції змінних
        output = redirected_output.getvalue()
        if output:
            print(f"[РЕЗУЛЬТАТ]:\n{output.strip()}")
            return output
        else:
            print("[РЕЗУЛЬТАТ]: Успішно, але без print().")
            return "Код виконано успішно, але нічого не виведено. Додай print()."
    except Exception as e:
        error_msg = f"Помилка виконання ({type(e).__name__}): {str(e)}"
        print(f"[ПОМИЛКА]: {error_msg}")
        return error_msg
    finally:
        sys.stdout = old_stdout

# --- 3. НАЛАШТУВАННЯ АГЕНТА ---
system_prompt = """
Ти — елітний AI-інженер та розробник. 
Твоя мета: писати скрипти для розв'язання інженерних, математичних та аналітичних задач.

Твої суворі правила:
1. НІКОЛИ не видавай код користувачу, поки не перевіриш його працездатність через `execute_python_code`.
2. Якщо отримуєш помилку після запуску, проаналізуй її, виправ код і запусти знову (Self-Correction).
3. Якщо тебе просять намалювати графік:
   - ВИКОРИСТОВУЙ numpy та matplotlib.
   - ЗАБОРОНЕНО використовувати plt.show().
   - ЗАВЖДИ зберігай графік як зображення: `plt.savefig('назва_файлу.png')`.
4. Завжди додавай `print()` у свій код, щоб вивести фінальні результати.
5. Після успішного виконання коду, коротко поясни користувачу логіку рішення та вкажи, де шукати збережені файли.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction=system_prompt,
    tools=[execute_python_code]
)

chat = model.start_chat(enable_automatic_function_calling=True)

# --- 4. ІНТЕРАКТИВНИЙ ІНТЕРФЕЙС (CLI) ---
def main():
    print("\n" + "="*50)
    print("🚀 AI Engineering Agent запущено!")
    print("Введіть ваше завдання (або 'exit' для виходу).")
    print("="*50)
    
    while True:
        try:
            user_input = input("\n[Ви]: ")
            if user_input.lower() in ['exit', 'quit', 'вихід']:
                print("Завершення роботи агента. До побачення!")
                break
            
            if not user_input.strip():
                continue

            print("\n[Агент]: Думаю та виконую...")
            response = chat.send_message(user_input)
            
            print("\n" + "="*50)
            print(f"✅ [ФІНАЛЬНА ВІДПОВІДЬ]:\n{response.text}")
            print("="*50)
            
        except KeyboardInterrupt:
            print("\nПроцес перервано користувачем. До побачення!")
            break
        except Exception as e:
            print(f"\n❌ Виникла критична помилка API: {e}")

if __name__ == "__main__":
    main()
