import cv2
import torch
from ultralytics import YOLO
import matplotlib.pyplot as plt

def predict_image(image_path):
    """Use the trained YOLO model to predict objects in the image"""
    
    # Load the trained YOLO modelmodel = YOLO(r'C:\MurthyLab\Project\Project\my_yolo_model2\weights\best.pt')
    model = YOLO(r"C:\MurthyLab\Project\Project\my_yolo_model2\weights\best.pt")


    
    # Run the model's inference on the image
    results = model(image_path)
    
    # If there are detections, show the image with bounding boxes
    if results[0].boxes:
        results[0].show()  # Display the image with bounding boxes
    else:
        print("No objects detected.")
    
    # Optionally, save the image with predictions
    output_image = results[0].plot()  # Use plot to generate the output image
    output_path = 'predicted_image.jpg'
    cv2.imwrite(output_path, output_image)  # Save the output image
    
    # Display the image with matplotlib (optional)
    plt.imshow(output_image)
    plt.axis('off')  # Hide axes
    plt.show()
    
    print(f"Prediction complete. Image saved at {output_path}")

# Example usage
predict_image(r"C:\MurthyLab\Project\Project\train\images\fa0ab21b-IMG_20240603_151452.jpg")
