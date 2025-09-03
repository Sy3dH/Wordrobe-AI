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

#### **Step 3: Auto-Cropping of the Generative Body**

* Given the photo, the main object is removed from the photo.
* It uses rembg package and uses a U-squared net to do SOD (Salient Object Detection)

#### **Step 4: Upscaling the Generative Body**

* Given the photo, the face and the body is upscaled.
* It uses realersgan and GFPGAN to improve the body and the face respectively.

#### **Step 5: Virtual Try-on** (In progress)

* Given the model and the clothing, the output image is saved showing the model wearing the clothes.
---

### **Checklist**

* [x] **Avatar Creation** →  `/avatar-creation` (Completed)
* [x] **Avatar Cropping** → `/crop-avatar` (Completed)
* [x] **Pose Validation for VTON Accuracy** (Completed)
* [x] **Upscaling of the Avatar** (Completed)
* [ ] **VTON (Virtual Try-On) of Clothes** (In-progress)

---

### **Project Structure**

```
wardrobe_ai/
├─ src/
│  ├─ configs/                  # Default configs for generation
│  ├─ routes/                   # API routes
│  ├─ crop/                     # Logic for cropping 
│  ├─ pose/                     # Logic for pose validation
|  ├─ output/                   # Generated outputs
│  ├─ prompts/                  # Prompt for generating 2D avatar
│  ├─ upscale/                  # Upscaling the image
│  ├─ avatar/                   # Avatar creation logic                   
├─ sample/                      # Sample input images -> Not in repository
├─ main.py                      # FastAPI entry point
├─ utils.py                     # Helper functions
└─ requirements.txt
```

### **Setup & Run**

0. **Checkout to development branch**
   All features are currently in the `development` branch.

   ```bash
   git checkout development
   ```

1. **Create and activate a virtual environment**
   Ensure you have **Python 3.9** installed.

   ```bash
   python3.9 -m venv venv
   source venv/bin/activate     # On macOS/Linux
   venv\Scripts\activate        # On Windows
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   Create a `.env` file in the project root:

   ```
   BFL_API_KEY=your_api_key_here
   ```

   To get the BFL API key, log in to [BFL](http://www.bfl.ai/).

4. **Run the API**

   ```bash
   uvicorn main:app --port 8000 --reload
   ```

   OpenAPI Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### **Available Endpoint**

#### `POST /avatar-creation`

* **Description**: Creates an avatar using the Flux-pro Kontext model.
* **Request**:

  * Form-data:

    * `image`: Frontal face photo (JPEG/PNG).
 * Output
   **Response:
   A generated full-body avatar image with accurate proportions.

   Response contains:
   ```
   {
     "status": "success",
     "avatar_url": "/output/avatar_123.png"
   }
   ```

#### `POST /crop-avatar`

* **Description**: Crops the main object out of the background.
* **Request**:

  * Form-data:

    * `image`: Image of the avatar (JPEG/PNG/WEBP).

 * Output
   **Response:
   Cropped avatar (background removed).

   Response contains:
   ```
   {
     "status": "success",
     "avatar_url": "/output/avatar_123.png"
   }
   ```

#### `POST /validate-pose`
* **Description**: Checks if the uploaded image is in A-pose (correct standing position for VTON).
* **Request**:
  * Form-data:
    * `image`: Image of the avatar (JPEG/PNG/WEBP).
* Output
  **Response:
   ```   
   {
        "is_apose": false,
        "obstructions": {
          "torso": true,
          "hips": false,
          "legs": false,
          "arms_crossing": false,
          "legs_crossing": true,
          "legs_on_torso": false,
          "sitting": false
        },
        "comments": "Obstructions detected."
      }
   ```
   
#### `POST /upscale-image`
* **Description**: Upscale an image according to the user desire (2x,4x ...).
* **Request**:
  * Form-data:
    * `image`: Image of the avatar (JPEG/PNG/WEBP).
    * `outscale`: int (4 is default)
    * `face_enhance`: boolean ( To enhance the pixelated face)
* Output
  **Response:
   ```   
   {
     "status": "success",
     "avatar_url": "/output/avatar_123.png"
   }
   ```





