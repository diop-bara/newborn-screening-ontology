# Ontology for Newborn Screening

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

### 1. Installation of GraphDB and Data Import
- Download and install GraphDB (with the license).
- Open GraphDB and register the license.
- Create a new repository named `screening_ontology`.
- Select the repository `screening_ontology`.
- Import the data.
  
  👉 For more details, refer to images 1 to 12.

---

### 2. Clone the repository
Open a terminal in the desired directory, clone the repository, and navigate into the directory.
```bash
git clone https://github.com/diop-bara/newborn-screening-ontology.git
cd newborn-screening-ontology
```

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
