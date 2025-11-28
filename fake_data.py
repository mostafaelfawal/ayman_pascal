from models.scale import ScaleDB

db = ScaleDB()

for i in range(501, 1000):
    print("Adding fake record...", i+1)
    db.add_scale(
        customer_name=f"عميل {i+1}",
        load_type="حمولة عامة",
        car_number=f"رقم السيارة {1000 + i}",
        governorate="القاهرة",
        first_time="10:00 AM",
        first_date="2024-01-01",
        first_weight=str(1000 + i * 10),
        last_time="02:00 PM",
        last_date="2024-01-01",
        last_weight=str(2000 + i * 10)
    )
