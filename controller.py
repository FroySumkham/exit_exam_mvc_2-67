import json
from datetime import datetime
from tkinter import messagebox
from model import Phoenix, Dragon, Owl, save_to_json

REJECTED_PETS_FILE = "rejected_pets.json"

def load_rejected_pets():
    try:
        with open(REJECTED_PETS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Phoenix": 0, "Dragon": 0, "Owl": 0}

def save_rejected_pets(data):
    with open(REJECTED_PETS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# โหลดจำนวนสัตว์ที่ถูกปฏิเสธจากไฟล์
rejected_pets_count = load_rejected_pets()

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y") 
        return True
    except ValueError:
        return False

def validate_positive_integer(value):
    return value.isdigit() and int(value) > 0

def validate_extra_value(pet_type, extra_value):
    if pet_type == "Phoenix":
        return extra_value in ["True", "False"]
    elif pet_type in ["Dragon", "Owl"]:
        return extra_value.isdigit() and int(extra_value) >= 0
    return False

def save_pet_to_json(pet_type, last_health_check, vaccines_received, extra_value):
    if not validate_extra_value(pet_type, extra_value):
        messagebox.showerror("ข้อผิดพลาด", f"ค่าของ {pet_type} ไม่ถูกต้อง!")
        return False
    
    if pet_type == "Phoenix" and extra_value != "True":
        rejected_pets_count["Phoenix"] += 1
        save_rejected_pets(rejected_pets_count)
        messagebox.showerror("ข้อผิดพลาด", "นกฟินิกซ์ต้องมีใบรับรองไฟไม่ลาม!")
        return False
    elif pet_type == "Dragon" and int(extra_value) > 70:
        rejected_pets_count["Dragon"] += 1
        save_rejected_pets(rejected_pets_count)
        messagebox.showerror("ข้อผิดพลาด", "มังกรที่มีระดับมลพิษควันเกิน 70% ไม่สามารถรับได้!")
        return False
    elif pet_type == "Owl" and int(extra_value) < 100:
        rejected_pets_count["Owl"] += 1
        save_rejected_pets(rejected_pets_count)
        messagebox.showerror("ข้อผิดพลาด", "นกฮูกต้องสามารถบินได้ไกลอย่างน้อย 100 km!")
        return False
    
    if not validate_date(last_health_check):
        messagebox.showerror("ข้อผิดพลาด", "รูปแบบวันที่ไม่ถูกต้อง! กรุณาใช้ Date Picker")
        return False
    
    if not validate_positive_integer(vaccines_received):
        messagebox.showerror("ข้อผิดพลาด", "จำนวนวัคซีนต้องเป็นจำนวนเต็มบวก!")
        return False
    
    formatted_date = datetime.strptime(last_health_check, "%d/%m/%Y").strftime("%d-%m-%Y")
    
    if pet_type == "Phoenix":
        pet = Phoenix(formatted_date, int(vaccines_received), True)
    elif pet_type == "Dragon":
        pet = Dragon(formatted_date, int(vaccines_received), int(extra_value))
    elif pet_type == "Owl":
        pet = Owl(formatted_date, int(vaccines_received), int(extra_value))
    else:
        messagebox.showerror("ข้อผิดพลาด", "ประเภทสัตว์เลี้ยงไม่ถูกต้อง!")
        return False
    
    save_to_json(pet)
    messagebox.showinfo("สำเร็จ", "เพิ่มสัตว์เลี้ยงสำเร็จ!")
    return True

def get_rejected_pets_report():
    return rejected_pets_count
