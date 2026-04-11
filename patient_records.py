"""
Patient Records for IV Monitoring System
Contains sample patient data with bed assignments, room information, and IV bottle capacities
"""

# Sample patient records with complete information
PATIENT_RECORDS = [
    {
        "patient_id": 1,
        "name": "John Doe",
        "bed_number": "ICU-01",
        "room_number": 101,
        "iv_bottle_capacity": 500,  # mL
        "status": "active",
        "admission_date": "2026-04-01",
    },
    {
        "patient_id": 2,
        "name": "Sarah Johnson",
        "bed_number": "ICU-02",
        "room_number": 101,
        "iv_bottle_capacity": 750,  # mL
        "status": "active",
        "admission_date": "2026-04-02",
    },
    {
        "patient_id": 3,
        "name": "Michael Chen",
        "bed_number": "ICU-03",
        "room_number": 102,
        "iv_bottle_capacity": 500,  # mL
        "status": "active",
        "admission_date": "2026-04-03",
    },
    {
        "patient_id": 4,
        "name": "Emily Rodriguez",
        "bed_number": "ICU-04",
        "room_number": 102,
        "iv_bottle_capacity": 1000,  # mL
        "status": "active",
        "admission_date": "2026-04-01",
    },
    {
        "patient_id": 5,
        "name": "David Williams",
        "bed_number": "ICU-05",
        "room_number": 103,
        "iv_bottle_capacity": 750,  # mL
        "status": "active",
        "admission_date": "2026-04-04",
    },
    {
        "patient_id": 6,
        "name": "Jessica Brown",
        "bed_number": "Ward-A-01",
        "room_number": 201,
        "iv_bottle_capacity": 500,  # mL
        "status": "active",
        "admission_date": "2026-04-02",
    },
    {
        "patient_id": 7,
        "name": "Robert Taylor",
        "bed_number": "Ward-A-02",
        "room_number": 201,
        "iv_bottle_capacity": 500,  # mL
        "status": "active",
        "admission_date": "2026-04-05",
    },
    {
        "patient_id": 8,
        "name": "Amanda Martinez",
        "bed_number": "Ward-A-03",
        "room_number": 202,
        "iv_bottle_capacity": 750,  # mL
        "status": "active",
        "admission_date": "2026-03-31",
    },
    {
        "patient_id": 9,
        "name": "Christopher Lee",
        "bed_number": "Ward-A-04",
        "room_number": 202,
        "iv_bottle_capacity": 1000,  # mL
        "status": "active",
        "admission_date": "2026-04-06",
    },
    {
        "patient_id": 10,
        "name": "Monica Patel",
        "bed_number": "Ward-B-01",
        "room_number": 301,
        "iv_bottle_capacity": 500,  # mL
        "status": "active",
        "admission_date": "2026-04-03",
    },
    {
        "patient_id": 11,
        "name": "Thomas Anderson",
        "bed_number": "Ward-B-02",
        "room_number": 301,
        "iv_bottle_capacity": 750,  # mL
        "status": "active",
        "admission_date": "2026-04-07",
    },
    {
        "patient_id": 12,
        "name": "Lisa Thompson",
        "bed_number": "Ward-B-03",
        "room_number": 302,
        "iv_bottle_capacity": 500,  # mL
        "status": "recovering",
        "admission_date": "2026-03-28",
    },
    {
        "patient_id": 13,
        "name": "James Garcia",
        "bed_number": "Ward-B-04",
        "room_number": 302,
        "iv_bottle_capacity": 1000,  # mL
        "status": "active",
        "admission_date": "2026-04-08",
    },
    {
        "patient_id": 14,
        "name": "Rachel White",
        "bed_number": "ICU-06",
        "room_number": 103,
        "iv_bottle_capacity": 1000,  # mL
        "status": "critical",
        "admission_date": "2026-04-05",
    },
    {
        "patient_id": 15,
        "name": "Kevin Smith",
        "bed_number": "Ward-C-01",
        "room_number": 303,
        "iv_bottle_capacity": 500,  # mL
        "status": "active",
        "admission_date": "2026-04-09",
    },
    {
        "patient_id": 16,
        "name": "Olivia Harris",
        "bed_number": "Ward-C-02",
        "room_number": 303,
        "iv_bottle_capacity": 750,  # mL
        "status": "active",
        "admission_date": "2026-04-06",
    },
]


def get_all_patients():
    """Retrieve all patient records"""
    return PATIENT_RECORDS


def get_patient_by_id(patient_id):
    """Retrieve a specific patient record by ID"""
    for patient in PATIENT_RECORDS:
        if patient["patient_id"] == patient_id:
            return patient
    return None


def get_patients_by_room(room_number):
    """Retrieve all patients in a specific room"""
    return [p for p in PATIENT_RECORDS if p["room_number"] == room_number]


def get_patients_by_status(status):
    """Retrieve all patients with a specific status"""
    return [p for p in PATIENT_RECORDS if p["status"] == status]


def get_patient_summary():
    """Get a summary of all patients"""
    return {
        "total_patients": len(PATIENT_RECORDS),
        "active_patients": len([p for p in PATIENT_RECORDS if p["status"] == "active"]),
        "critical_patients": len([p for p in PATIENT_RECORDS if p["status"] == "critical"]),
        "recovering_patients": len([p for p in PATIENT_RECORDS if p["status"] == "recovering"]),
    }


# Display patient records in a formatted table
if __name__ == "__main__":
    print("=" * 100)
    print(f"{'Patient ID':<12} {'Name':<20} {'Bed Number':<12} {'Room':<8} {'IV Capacity (mL)':<18} {'Status':<12}")
    print("=" * 100)
    
    for patient in PATIENT_RECORDS:
        print(
            f"{patient['patient_id']:<12} "
            f"{patient['name']:<20} "
            f"{patient['bed_number']:<12} "
            f"{patient['room_number']:<8} "
            f"{patient['iv_bottle_capacity']:<18} "
            f"{patient['status']:<12}"
        )
    
    print("=" * 100)
    print(f"\nSummary: {get_patient_summary()}")
