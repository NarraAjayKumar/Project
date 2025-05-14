import os
import shutil
import yaml
from sklearn.model_selection import train_test_split 
from ultralytics import YOLO

def prepare_yolo_dataset():
    """Organize images and labels into YOLO training structure"""
    
    # Create train/val directories if they don't exist
    os.makedirs('train/images', exist_ok=True)
    os.makedirs('train/labels', exist_ok=True)
    os.makedirs('val/images', exist_ok=True)
    os.makedirs('val/labels', exist_ok=True)
    
    # Get all image files from dataset/images
    image_files = [f for f in os.listdir('dataset/images') if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    
    # Split into train/val (80/20)
    train_files, val_files = train_test_split(image_files, test_size=0.2, random_state=42)
    
    # Helper function to copy files
    def copy_files(files, split):
        for file in files:
            # Copy image
            shutil.copy2(f'dataset/images/{file}', f'{split}/images/{file}')
            
            # Copy corresponding label
            label_file = os.path.splitext(file)[0] + '.txt'
            if os.path.exists(f'dataset/labels/{label_file}'):
                shutil.copy2(f'dataset/labels/{label_file}', f'{split}/labels/{label_file}')
    
    # Copy files to respective directories
    copy_files(train_files, 'train')
    copy_files(val_files, 'val')
    
    print(f"Dataset prepared with {len(train_files)} training and {len(val_files)} validation images")

def train_yolo_model():
    """Train YOLO model on the prepared dataset"""
    
    # ✅ Corrected path to classes.txt
    with open('dataset/classes.txt') as f:
        classes = [line.strip() for line in f.readlines() if line.strip()]
    
    # Create data.yaml configuration
    data_config = {
        'train': os.path.abspath('train/images'),
        'val': os.path.abspath('val/images'),
        'nc': len(classes),
        'names': classes
    }
    
    with open('data.yaml', 'w') as f:
        yaml.dump(data_config, f)
    
    # Load pretrained model
    model = YOLO('yolov8n.pt')  # Using nano version
    
    # Train the model
    results = model.train(
        data='data.yaml',
        epochs=10,
        imgsz=640,
        batch=16,
        name='my_yolo_model'
    )
    
    return model

if __name__ == '__main__':
    # Step 1: Prepare dataset
    print("Preparing dataset...")
    prepare_yolo_dataset()
    
    # Step 2: Train model
    print("\nStarting training...")
    model = train_yolo_model()
    
    # Step 3: Export the trained model to ONNX format
    model.export(format='onnx')
    print("\nTraining complete! Model saved as 'my_yolo_model'")
