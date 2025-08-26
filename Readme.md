## **Wardrobe AI**

Wardrobe AI is a FastAPI-based service that uses generative AI to create personalized avatars from photos and prepare them for virtual try-on (VTON). 
It leverages the **Flux-pro Kontext** model for generative body completion.

### **Current Workflow**

#### **Step 1: Photo Input**

* User provides a **frontal face photo**.

#### **Step 2: Generative Body Completion**

* Takes the face photo and generatively fills the complete body.
* Adds default clothing while maintaining accurate size and proportions.
* Powered by **Flux-pro Kontext**.

---

### **Checklist**

* [x] **Avatar Creation** → `/avatar-creation` (Completed)
* [x] **Avatar Cropping** (Completed)
* [ ] **VTON (Virtual Try-On) of Clothes**
* [ ] **Pose Validation for VTON Accuracy**

---

### **Project Structure**

```
wardrobe_ai/
├─ src/
│  ├─ configs/                  # Default configs for generation
│  ├─ routes/                   # API routes
│  ├─ avatar/                   # Avatar creation logic                   
├─ output/                      # Generated outputs
├─ sample/                      # Sample input images
├─ main.py                      # FastAPI entry point
├─ utils.py                     # Helper functions
└─ requirements.txt
```

---

### **Setup & Run**

0. **Checkout to feature-branch**
   All the features currently are in the feature-branch. So checkout to that.

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   Create a `.env` file:

   ```
   BFL_API_KEY=your_api_key_here
   ```

3. **Run the API**

   ```bash
   uvicorn main:app --port 8000 --reload
   ```

   * OpenAPI Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### **Available Endpoint**

#### `POST /avatar-creation`

* **Description**: Creates an avatar using the Flux-pro Kontext model.
* **Request**:

  * Form-data:

    * `image`: Frontal face photo (JPEG/PNG).


