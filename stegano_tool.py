import os
import base64
from stegano import lsb

# Визначаємо шлях до папки
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_png_files():
    return [f for f in os.listdir(BASE_DIR) if f.endswith('.png')]

def select_file():
    files = get_png_files()
    if not files:
        print("❌ У папці немає жодного .png файлу!")
        return None
    
    print("\n📁 Знайдені зображення:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")
    
    try:
        choice = int(input("\nОбери номер файлу: "))
        if 1 <= choice <= len(files):
            return os.path.join(BASE_DIR, files[choice-1])
        else:
            print("🤡 Такого номера немає в списку.")
    except ValueError:
        print("⚠️ Введи число, а не літери.")
    return None

def hide_message():
    image_path = select_file()
    if not image_path: return

    secret_text = input("📝 Введіть секретне повідомлення: ")
    output_name = input("💾 Як назвати новий файл? (напр. secret.png): ")
    
    if not output_name.lower().endswith('.png'):
        output_name += '.png'
        print(f"🔧 (Автоматично додано розширення: {output_name})")

    output_path = os.path.join(BASE_DIR, output_name)

    print("⏳ Маскуємо дані...")
    
    b64_secret = base64.b64encode(secret_text.encode('utf-8')).decode('utf-8')
    
    secret_image = lsb.hide(image_path, b64_secret)
    secret_image.save(output_path)
    print(f"✅ Готово! Секрет сховано у: {output_path}")

def reveal_message():
    image_path = select_file()
    if not image_path: return

    print("🔍 Скануємо пікселі...")
    try:
        secret = lsb.reveal(image_path)
        if secret:
            try:
                decoded_secret = base64.b64decode(secret).decode('utf-8')
                print(f"\n🔓 ЗНАЙДЕНО СЕКРЕТ: >>> {decoded_secret} <<<\n")
            except:
                print(f"\n🔓 ЗНАЙДЕНО СЕКРЕТ: >>> {secret} <<<\n")
        else:
            print("📭 У цій картинці нічого не сховано.")
    except Exception:
        print("📭 Тут нічого немає, або файл було стиснуто.")

if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        print("🕵️‍♂️ STEGANO-TOOL🕵️‍♂️")
        print("="*40)
        print("1. Сховати дані")
        print("2. Прочитати дані")
        print("0. Вихід")
        
        cmd = input("\nОбери дію: ")
        if cmd == '1': hide_message()
        elif cmd == '2': reveal_message()
        elif cmd == '0': break