Diabetic Retinopathy Detection AI 🧠🩸

A modern AI application for diabetic retinopathy detection from retinal fundus images using deep learning, featuring multi-class classification, evaluation metrics, and single-image prediction.

✨ Features
🤖 AI-Powered Detection – Uses TensorFlow and EfficientNetB0 for image classification
💻 Multi-Class Classification – Predicts 17 DR-related classes
📊 Evaluation Metrics – Accuracy, AUC, and loss tracking
🖼️ Single Image Prediction – Upload a retinal image for DR prediction
🗂️ Dataset Handling – Integrated with Roboflow dataset download
🎨 Clean & Modular Code – Easy to extend and retrain models

🛠️ Tech Stack

Backend / Model Training

Python 3.8+

TensorFlow 2.x

Keras

OpenCV, NumPy, Pandas

Roboflow API

Frontend / Visualization

Jupyter Notebook / Python scripts

Matplotlib / Seaborn

🚀 Quick Start

Prerequisites

Python 3.8 or higher

pip

Roboflow API Key

1. Clone the Repository
git clone https://github.com/yourusername/diabetic-retinopathy-ai.git
cd diabetic-retinopathy-ai

2. Install Dependencies
pip install -r requirements.txt

3. Dataset Setup
from roboflow import Roboflow

rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("diabetic-retinopathy-efigv").project("diabetic-retinopathy-hvhiu")
dataset = project.version(1).download("multiclass")

4. Train the Model
python scripts/train_model.py

5. Evaluate Model
python scripts/evaluate_model.py

6. Predict Single Image
python scripts/predict_single_image.py --image path/to/image.jpg


📖 Scripts / API

Script	Description
train_model.py	Train model on DR dataset
evaluate_model.py	Evaluate model performance
predict_single_image.py	Predict DR class for a single image

🔧 Configuration

Variable	Description	Default
ROBOFLOW_API_KEY	Your Roboflow API key	Required
DATASET_PATH	Optional local dataset path	None
BATCH_SIZE	Training batch size	32
EPOCHS	Number of training epochs	50
LEARNING_RATE	Learning rate for optimizer	0.001

🏗️ Project Structure

diabetic-retinopathy-ai/
├── dataset/                
│   ├── train/
│   ├── valid/
│   └── test/
├── models/                 
├── scripts/
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── predict_single_image.py
├── notebooks/              
├── requirements.txt
└── README.md


🤝 Contributing

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📝 License
This project is licensed under the MIT License – see the LICENSE file for details.

🙏 Acknowledgments

Roboflow
 for dataset management

TensorFlow / Keras for deep learning framework

EfficientNet authors for backbone architecture

📞 Support
If you have any questions or need help, open an issue on GitHub.
