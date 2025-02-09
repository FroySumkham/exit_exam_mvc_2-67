import tkinter as tk
import json
from datetime import datetime
from tkinter import messagebox
from tkcalendar import DateEntry
from controller import save_pet_to_json, get_rejected_pets_report
from model import get_accepted_pets_report

def show_main_menu():
    root = tk.Tk()
    root.title("ระบบจัดการสัตว์เลี้ยงเวทมนตร์")
    root.geometry("800x500")

    tk.Label(root, text="=== ระบบจัดการสัตว์เลี้ยงเวทมนตร์ ===", font=("Arial", 30)).pack(pady=20)
    
    tk.Button(root, text="เพิ่มสัตว์เลี้ยง", command=add_pet_menu, width=30, font=("Arial", 14)).pack(pady=5)
    tk.Button(root, text="แสดงรายการสัตว์เลี้ยง", command=select_pet_display_mode, width=30, font=("Arial", 14)).pack(pady=5)
    tk.Button(root, text="รายงานสรุปสัตว์เลี้ยง", command=show_report, width=30, font=("Arial", 14)).pack(pady=5)
    tk.Button(root, text="ออกจากระบบ", command=root.quit, width=30, font=("Arial", 14)).pack(pady=5)
    
    root.mainloop()
def add_pet_menu():
    pet_window = tk.Toplevel()
    pet_window.title("เพิ่มสัตว์เลี้ยง")
    pet_window.geometry("600x400")
    
    tk.Label(pet_window, text="เลือกประเภทสัตว์เลี้ยง:", font=("Arial", 18)).pack()
    pet_type_var = tk.StringVar(value="Phoenix")
    tk.OptionMenu(pet_window, pet_type_var, "Phoenix", "Dragon", "Owl").pack()
    
    tk.Button(pet_window, text="ถัดไป", command=lambda: get_pet_data(pet_window, pet_type_var.get())).pack(pady=10)

def get_pet_data(window, pet_type):
    window.destroy()
    data_window = tk.Toplevel()
    data_window.title(f"เพิ่ม {pet_type}")
    data_window.geometry("600x400")
    
    tk.Label(data_window, text="วันที่ตรวจสุขภาพล่าสุด:", font=("Arial", 14)).pack()
    health_entry = DateEntry(data_window, date_pattern='dd/MM/yyyy') 
    health_entry.pack()
    
    tk.Label(data_window, text="จำนวนวัคซีนที่ได้รับแล้ว:", font=("Arial", 14)).pack()
    vaccine_entry = tk.Entry(data_window)
    vaccine_entry.pack()
    
    extra_var = tk.StringVar()
    if pet_type == "Phoenix":
        tk.Label(data_window, text="มีใบรับรองไฟไม่ลาม?", font=("Arial", 14)).pack()
        extra_entry = tk.OptionMenu(data_window, extra_var, "True", "False")
    elif pet_type == "Dragon":
        tk.Label(data_window, text="ระดับมลพิษที่เกิดจากควัน (%):", font=("Arial", 14)).pack()
        extra_entry = tk.Entry(data_window, textvariable=extra_var)
    elif pet_type == "Owl":
        tk.Label(data_window, text="ระยะทางบินได้โดยไม่ทานข้าว (km):", font=("Arial", 14)).pack()
        extra_entry = tk.Entry(data_window, textvariable=extra_var)
    
    extra_entry.pack()
    
    tk.Button(data_window, text="บันทึก", command=lambda: save_and_close(data_window, pet_type, health_entry.get(), vaccine_entry.get(), extra_var.get())).pack(pady=10)

def save_and_close(window, pet_type, last_health_check, vaccines_received, extra_value):
    success = save_pet_to_json(pet_type, last_health_check, vaccines_received, extra_value)
    if success:
        window.destroy()


def show_report():
    report_window = tk.Toplevel()
    report_window.title("รายงานสรุปสัตว์เลี้ยง")
    report_window.geometry("600x400")

    accepted_pets = get_accepted_pets_report()
    rejected_pets = get_rejected_pets_report()

    tk.Label(report_window, text="=== รายงานสรุปสัตว์เลี้ยง ===", font=("Arial", 18)).pack(pady=10)
    
    tk.Label(report_window, text=f"นกฟินิกซ์ที่รับเข้า: {accepted_pets['Phoenix']} | ปฏิเสธ: {rejected_pets['Phoenix']}", font=("Arial", 12)).pack()
    tk.Label(report_window, text=f"มังกรที่รับเข้า: {accepted_pets['Dragon']} | ปฏิเสธ: {rejected_pets['Dragon']}", font=("Arial", 12)).pack()
    tk.Label(report_window, text=f"นกฮูกที่รับเข้า: {accepted_pets['Owl']} | ปฏิเสธ: {rejected_pets['Owl']}", font=("Arial", 12)).pack()

    total_accepted = sum(accepted_pets.values())
    total_rejected = sum(rejected_pets.values())

    tk.Label(report_window, text=f"สัตว์ที่ถูกรับเข้าโรงเรียนทั้งหมด: {total_accepted}", font=("Arial", 14, "bold")).pack(pady=5)
    tk.Label(report_window, text=f"สัตว์ที่ถูกปฏิเสธทั้งหมด: {total_rejected}", font=("Arial", 14, "bold"), fg="red").pack(pady=5)

def select_pet_display_mode():
    mode_window = tk.Toplevel()
    mode_window.title("เลือกโหมดการแสดงสัตว์เลี้ยง")
    mode_window.geometry("600x400")
    
    tk.Label(mode_window, text="เลือกโหมดการแสดงสัตว์เลี้ยง:", font=("Arial", 18)).pack()
    
    tk.Button(mode_window, text="แสดงทั้งหมด", command=lambda: display_pets("รวม"), width=20, font=("Arial", 14)).pack(pady=5)
    tk.Button(mode_window, text="แยกตามประเภท", command=show_pets_by_type, width=20, font=("Arial", 14)).pack(pady=5)

def show_pets_by_type():
    type_window = tk.Toplevel()
    type_window.title("เลือกประเภทสัตว์")
    type_window.geometry("600x400")
    
    tk.Label(type_window, text="เลือกประเภทสัตว์เลี้ยงที่ต้องการแสดง:", font=("Arial", 18)).pack()
    pet_type_var = tk.StringVar(value="Phoenix")
    tk.OptionMenu(type_window, pet_type_var, "Phoenix", "Dragon", "Owl").pack()
    
    tk.Button(type_window, text="แสดง", command=lambda: display_pets(pet_type_var.get())).pack(pady=10)

def display_pets(filter_type):
    pets_window = tk.Toplevel()
    pets_window.title(f"รายการสัตว์เลี้ยง ({filter_type})")
    pets_window.geometry("600x400")
    
    tk.Label(pets_window, text=f"=== รายการสัตว์เลี้ยง ({filter_type}) ===", font=("Arial", 18)).pack(pady=10)
    
    try:
        with open("pets.json", "r", encoding="utf-8") as file:
            pets_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pets_data = []
    
    filtered_pets = [pet for pet in pets_data if filter_type == "รวม" or pet['type'] == filter_type]
    
    if not filtered_pets:
        tk.Label(pets_window, text="ไม่มีข้อมูลสัตว์เลี้ยงในระบบ").pack()
    else:
        for pet in filtered_pets:
            date_str = datetime.strptime(pet['last_health_check'], "%d-%m-%Y").strftime("%d-%m-%Y")
            pet_info = f"ID: {pet['id']} | ประเภท: {pet['type']} | ตรวจสุขภาพ: {date_str} | วัคซีน: {pet['vaccines_received']}"
            tk.Label(pets_window, text=pet_info, font=("Arial", 14)).pack()

def show_message(message):
    messagebox.showinfo("แจ้งเตือน", message)

if __name__ == "__main__":
    show_main_menu()
