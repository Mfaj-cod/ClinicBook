# data.py - add doctor entries here, then run `python seed.py`
doctors_data = [
    {
        "name": "Dr. Anjali Mehta",
        "specialization": "Dermatologist",
        "clinic": "SkinGlow Clinic",
        "city": "Delhi",
        "address": "A-12, Saket",
        "fees": 500,
        "email": "anjali.mehta@example.com",
        "phone": "+91-9810001111",
        "about": "Cosmetic & clinical dermatology. MBBS, MD Dermatology."
    },
    {
        "name": "Dr. Arjun Patel",
        "specialization": "Cardiologist",
        "clinic": "HeartCare Hospital",
        "city": "Mumbai",
        "address": "23/B, Bandra West",
        "fees": 1200,
        "email": "arjun.patel@example.com",
        "phone": "+91-9820002222",
        "about": "Interventional cardiologist with 15 years experience."
    },
    {
        "name": "Dr. Kavita Sharma",
        "specialization": "Pediatrician",
        "clinic": "Happy Kids Clinic",
        "city": "Bangalore",
        "address": "45, MG Road",
        "fees": 700,
        "email": "kavita.sharma@example.com",
        "phone": "+91-9830003333",
        "about": "Child health specialist with 10 years experience."
    },
    {
        "name": "Dr. Sameer Khan",
        "specialization": "Orthopedic Surgeon",
        "clinic": "BoneCare Clinic",
        "city": "Hyderabad",
        "address": "12, Jubilee Hills",
        "fees": 900,
        "email": "sameer.khan@example.com",
        "phone": "+91-9840004444",
        "about": "Expert in joint replacement and sports injuries."
    },
    {
        "name": "Dr. Priya Desai",
        "specialization": "Gynecologist",
        "clinic": "Women's Care Clinic",
        "city": "Pune",
        "address": "78, Kalyani Nagar",
        "fees": 800,
        "email": "priya.desai@example.com",
        "phone": "+91-9850005555",
        "about": "Specialist in obstetrics and gynecology with 12 years experience."
    },
    {
        "name": "Dr. Ramesh Gupta",
        "specialization": "Neurologist",
        "clinic": "BrainCare Center",
        "city": "Chennai",
        "address": "56, T Nagar",
        "fees": 1100,
        "email": "ramesh.gupta@example.com",
        "phone": "+91-9860006666",
        "about": "Expert in neurological disorders with 18 years experience."
    },
    {
        "name": "Dr. Neha Joshi",
        "specialization": "Psychiatrist",
        "clinic": "MindCare Clinic",
        "city": "Ahmedabad",
        "address": "89, CG Road",
        "fees": 950,
        "email": "neha.joshi@example.com",
        "phone": "+91-9870007777",
        "about": "Specialist in mental health with 14 years experience."
    },
    {
        "name": "Dr. Vikram Singh",
        "specialization": "General Physician",
        "clinic": "City Health Clinic",
        "city": "New Delhi",
        "address": "101, Connaught Place",
        "fees": 600,
        "email": "vikram.singh@example.com",
        "phone": "+91-9880008888",
        "about": "Experienced general physician with a focus on preventive care."
    },
    {
        "name": "Dr. Aisha Khan",
        "specialization": "Endocrinologist",
        "clinic": "HealthFirst Clinic",
        "city": "Kolkata",
        "address": "22, Park Street",
        "fees": 1000,
        "email": "aisha.khan@example.com",
        "phone": "+91-9890009999",
        "about": "Specialist in hormonal disorders with 12 years experience."
    },
    {
        "name": "Dr. Rohit Verma",
        "specialization": "ENT Specialist",
        "clinic": "Ear Nose Throat Clinic",
        "city": "Lucknow",
        "address": "17, Hazratganj",
        "fees": 650,
        "email": "rohit.verma@example.com",
        "phone": "+91-9900011111",
        "about": "ENT specialist with 11 years of clinical experience."
    },
    {
        "name": "Dr. Sunita Rao",
        "specialization": "Ophthalmologist",
        "clinic": "Vision Plus Eye Care",
        "city": "Jaipur",
        "address": "201, MI Road",
        "fees": 800,
        "email": "sunita.rao@example.com",
        "phone": "+91-9910022222",
        "about": "Cataract and refractive surgery specialist."
    },
    {
        "name": "Dr. Manoj Pillai",
        "specialization": "Gastroenterologist",
        "clinic": "Digestive Health Center",
        "city": "Thiruvananthapuram",
        "address": "33, MG Road",
        "fees": 1100,
        "email": "manoj.pillai@example.com",
        "phone": "+91-9920033333",
        "about": "Expert in liver and digestive diseases."
    },
    {
        "name": "Dr. Shalini Nair",
        "specialization": "Pulmonologist",
        "clinic": "BreatheWell Clinic",
        "city": "Kochi",
        "address": "12, Marine Drive",
        "fees": 900,
        "email": "shalini.nair@example.com",
        "phone": "+91-9930044444",
        "about": "Specialist in asthma and respiratory disorders."
    },
    {
        "name": "Dr. Deepak Sinha",
        "specialization": "Urologist",
        "clinic": "UroCare Hospital",
        "city": "Patna",
        "address": "88, Boring Road",
        "fees": 1200,
        "email": "deepak.sinha@example.com",
        "phone": "+91-9940055555",
        "about": "Urology and kidney stone specialist."
    },
    {
        "name": "Dr. Meera Iyer",
        "specialization": "Oncologist",
        "clinic": "Hope Cancer Center",
        "city": "Bengaluru",
        "address": "5, Indiranagar",
        "fees": 1500,
        "email": "meera.iyer@example.com",
        "phone": "+91-9950066666",
        "about": "Medical oncologist with 13 years experience."
    },
    {
        "name": "Dr. Rajesh Chawla",
        "specialization": "Nephrologist",
        "clinic": "Kidney Care Clinic",
        "city": "Chandigarh",
        "address": "44, Sector 17",
        "fees": 1300,
        "email": "rajesh.chawla@example.com",
        "phone": "+91-9960077777",
        "about": "Specialist in kidney diseases and dialysis."
    },
    {
        "name": "Dr. Farah Siddiqui",
        "specialization": "Rheumatologist",
        "clinic": "Joint Relief Clinic",
        "city": "Bhopal",
        "address": "67, Arera Colony",
        "fees": 950,
        "email": "farah.siddiqui@example.com",
        "phone": "+91-9970088888",
        "about": "Expert in arthritis and autoimmune diseases."
    },
    {
        "name": "Dr. Suresh Menon",
        "specialization": "Dentist",
        "clinic": "Smile Dental Studio",
        "city": "Goa",
        "address": "21, Panaji Market",
        "fees": 500,
        "email": "suresh.menon@example.com",
        "phone": "+91-9980099999",
        "about": "Cosmetic and restorative dentistry specialist."
    },
    {
        "name": "Dr. Pooja Agarwal",
        "specialization": "Ophthalmologist",
        "clinic": "ClearView Eye Hospital",
        "city": "Indore",
        "address": "9, Race Course Road",
        "fees": 850,
        "email": "pooja.agarwal@example.com",
        "phone": "+91-9990010101",
        "about": "Specialist in cataract and glaucoma management."
    },
    {
        "name": "Dr. Amitabh Roy",
        "specialization": "Plastic Surgeon",
        "clinic": "Aesthetica Clinic",
        "city": "Kolkata",
        "address": "55, Salt Lake",
        "fees": 2000,
        "email": "amitabh.roy@example.com",
        "phone": "+91-9001122334",
        "about": "Cosmetic and reconstructive surgery expert."
    }
]