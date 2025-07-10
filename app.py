# นำเข้าไลบรารีที่จำเป็น
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import GPUtil as GPU
import time

# สร้างอินสแตนซ์ของ FastAPI
app = FastAPI()

# ตั้งค่าไดเรกทอรีสำหรับเทมเพลต Jinja2
templates = Jinja2Templates(directory="templates")

# ฟังก์ชันสำหรับดึงข้อมูล GPU แบบเรียลไทม์
def get_realtime_gpu_info():
    try:
        # ดึงข้อมูล GPU ทั้งหมด
        gpus = GPU.getGPUs()
        gpu_data = []
        # วนลูปเพื่อจัดรูปแบบข้อมูลของ GPU แต่ละตัว
        for gpu in gpus:
            gpu_data.append({
                'id': gpu.id,
                'name': gpu.name,
                'load_percent': f'{gpu.load*100:.2f}',
                'load_raw': gpu.load * 100,
                'memory_used': f'{gpu.memoryUsed:.2f}',
                'memory_total': f'{gpu.memoryTotal:.2f}',
                'memory_util_percent': f'{gpu.memoryUtil*100:.2f}',
                'memory_util_raw': gpu.memoryUtil * 100,
                'temperature': f'{gpu.temperature:.0f}',
                'temperature_raw': gpu.temperature # เพิ่มค่าอุณหภูมิแบบดิบ
            })
        return gpu_data
    except Exception as e:
        # คืนค่าข้อผิดพลาดหากไม่สามารถดึงข้อมูลได้
        return [{'error': str(e)}]

# สร้าง API endpoint สำหรับข้อมูล GPU
@app.get("/api/gpu")
async def api_gpu_info():
    """
    API endpoint ที่ส่งคืนข้อมูล GPU ในรูปแบบ JSON
    """
    return get_realtime_gpu_info()

# สร้าง route หลักสำหรับแสดงหน้าเว็บ
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    แสดงหน้าเว็บหลัก (index.html) พร้อมข้อมูล GPU
    """
    gpu_info = get_realtime_gpu_info()
    return templates.TemplateResponse("index.html", {"request": request, "gpus": gpu_info})
