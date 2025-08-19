# 🧬 Ontology for Newborn Screening

## 📌 Prerequisites

Before running the project, make sure you have:  

- **Python**: version 3.9 or higher  
- **Conda** or another virtual environment manager  
- **GraphDB** installed and accessible  
- The following Python packages installed in the `screening_env` environment:  
  - `fastapi`  
  - `SPARQLWrapper`  
  - `uvicorn`  

---

## 📌 Usage

### 1. Clone the repository
```bash
git clone https://github.com/diop-bara/newborn-screening-ontology.git
cd newborn-screening-ontology
```

---

### 2. Import the ontology and data
- Import the ontology and the files in the [`data/`](./data) folder into **GraphDB**.  
- Refer to [`parametres_importation.png`](./parametres_importation.png) for import settings.  

---

### 3. Activate the virtual environment
On Windows, activate the `screening_env` environment with:

```bash
.\screening_env\Scripts\activate
```

---

### 4. Run the application
```bash
python app.py
```

---

### 5. Test the REST API

- Once the server is running, open the URL shown in the terminal (default: http://127.0.0.1:8000).
- Consult the following URL:
```bash
http://127.0.0.1:8000/newborn/Newborn_001
```
- You will receive a JSON response from the REST API.
