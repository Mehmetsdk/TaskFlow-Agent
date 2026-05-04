import json


def calendar_check(date_range: str) -> str:
    """Belirtilen tarih aralığı için takvim müsaitliğini kontrol eder."""
    print(f"🔧 [ARAÇ TETİKLENDİ]: Takvim kontrol ediliyor -> {date_range}")
    return json.dumps(
        {
            "status": "success",
            "available": True,
            "message": f"{date_range} tarihleri arasında takviminiz müsait.",
        }
    )


def search_service(query: str) -> str:
    """İstenen konsept, mekan veya hizmet için arama yapar."""
    print(f"🔧 [ARAÇ TETİKLENDİ]: Arama yapılıyor -> {query}")
    return json.dumps(
        {
            "status": "success",
            "results": [
                f"Seçenek 1: {query} (Bütçe dostu, yüksek puanlı)",
                f"Seçenek 2: {query} (Premium, merkezi konum)",
            ],
        }
    )


def booking_service(option: str) -> str:
    """Belirtilen seçenek için rezervasyon veya satın alma işlemini gerçekleştirir."""
    print(f"🔧 [ARAÇ TETİKLENDİ]: Rezervasyon yapılıyor -> {option}")
    return json.dumps(
        {
            "status": "success",
            "booking_ref": "BKG-778899",
            "message": f"'{option}' başarıyla rezerve edildi.",
        }
    )


def reminder_create(details: str) -> str:
    """Gerçekleşen işlemler için takvime hatırlatıcı ekler."""
    print(f"🔧 [ARAÇ TETİKLENDİ]: Hatırlatıcı kuruluyor -> {details}")
    return json.dumps({"status": "success", "message": f"Hatırlatıcı başarıyla eklendi: {details}"})


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calendar_check",
            "description": "Check if the user's calendar is free for a specific date or time range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_range": {
                        "type": "string",
                        "description": "The date or time range to check (e.g., 'next Tuesday afternoon', '2023-11-15').",
                    }
                },
                "required": ["date_range"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_service",
            "description": "Search for flights, hotels, coworking spaces, or any other services.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The specific search query (e.g., '3 coworking spaces in Warsaw under $20/day').",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "booking_service",
            "description": "Book an appointment, a trip, or a specific space.",
            "parameters": {
                "type": "object",
                "properties": {
                    "option": {
                        "type": "string",
                        "description": "The exact option or details to book.",
                    }
                },
                "required": ["option"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reminder_create",
            "description": "Create a calendar reminder for a specific event or booking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "details": {
                        "type": "string",
                        "description": "Details of the reminder to be created.",
                    }
                },
                "required": ["details"],
            },
        },
    },
]

AVAILABLE_TOOLS = {
    "calendar_check": calendar_check,
    "search_service": search_service,
    "booking_service": booking_service,
    "reminder_create": reminder_create,
}
