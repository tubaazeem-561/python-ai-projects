"""
Real-time Emotion Detection System
Detects 7 emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
"""

import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import urllib.request
import os

# Download pre-trained emotion detection model if not exists
MODEL_PATH = 'emotion_model.hdf5'
HAARCASCADE_PATH = 'haarcascade_frontalface_default.xml'

def download_model():
    """Download the pre-trained emotion detection model"""
    if not os.path.exists(MODEL_PATH):
        print("Downloading emotion detection model...")
        model_url = "https://github.com/oarriaga/face_classification/raw/master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5"
        try:
            urllib.request.urlretrieve(model_url, MODEL_PATH)
            print("Model downloaded successfully!")
        except Exception as e:
            print(f"Error downloading model: {e}")
            print("Please download the model manually from:")
            print(model_url)
            return False
    return True

def download_haarcascade():
    """Download Haar Cascade for face detection"""
    if not os.path.exists(HAARCASCADE_PATH):
        print("Downloading Haar Cascade for face detection...")
        haarcascade_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        try:
            urllib.request.urlretrieve(haarcascade_url, HAARCASCADE_PATH)
            print("Haar Cascade downloaded successfully!")
        except Exception as e:
            print(f"Error downloading Haar Cascade: {e}")
            return False
    return True

class EmotionDetector:
    def __init__(self):
        # Emotion labels
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        
        # Load the pre-trained emotion detection model
        if download_model() and download_haarcascade():
            try:
                self.emotion_model = load_model(MODEL_PATH, compile=False)
                self.face_cascade = cv2.CascadeClassifier(HAARCASCADE_PATH)
                print("Model and face detector loaded successfully!")
            except Exception as e:
                print(f"Error loading model: {e}")
                print("\nAlternative: Using a simpler approach without pre-trained model")
                self.emotion_model = None
                self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        else:
            print("Using OpenCV's built-in Haar Cascade")
            self.emotion_model = None
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_emotion(self, frame):
        """Detect emotions in the given frame"""
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if self.emotion_model is not None:
                # Extract the face ROI
                roi_gray = gray[y:y+h, x:x+w]
                
                # Preprocess the face for emotion detection
                roi = cv2.resize(roi_gray, (64, 64))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                
                # Predict emotion
                try:
                    prediction = self.emotion_model.predict(roi, verbose=0)[0]
                    emotion_idx = np.argmax(prediction)
                    emotion = self.emotion_labels[emotion_idx]
                    confidence = prediction[emotion_idx] * 100
                    
                    # Display emotion and confidence
                    text = f"{emotion}: {confidence:.2f}%"
                    cv2.putText(frame, text, (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Display all emotion probabilities
                    y_offset = y + h + 20
                    for i, (label, prob) in enumerate(zip(self.emotion_labels, prediction)):
                        prob_text = f"{label}: {prob*100:.1f}%"
                        cv2.putText(frame, prob_text, (x, y_offset + i*20),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                except Exception as e:
                    cv2.putText(frame, "Face Detected", (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                # If no model, just show face detected
                cv2.putText(frame, "Face Detected", (x, y-10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame
    
    def run(self):
        """Run the emotion detection on webcam feed"""
        # Start webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        print("\n" + "="*50)
        print("EMOTION DETECTION SYSTEM")
        print("="*50)
        print("Press 'q' to quit")
        print("Press 's' to take a screenshot")
        print("="*50 + "\n")
        
        screenshot_count = 0
        
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Detect emotions
            frame = self.detect_emotion(frame)
            
            # Display the resulting frame
            cv2.imshow('Emotion Detection - Press Q to Quit', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                screenshot_count += 1
                filename = f'emotion_screenshot_{screenshot_count}.jpg'
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved: {filename}")
        
        # Release everything
        cap.release()
        cv2.destroyAllWindows()
        print("\nEmotion detection stopped.")

def main():
    """Main function to run emotion detection"""
    print("Initializing Emotion Detection System...")
    print("\nRequired packages:")
    print("- opencv-python")
    print("- tensorflow/keras")
    print("- numpy")
    print("\nIf you get errors, install with:")
    print("pip install opencv-python tensorflow numpy")
    print("\n" + "-"*50 + "\n")
    
    detector = EmotionDetector()
    detector.run()

if __name__ == "__main__":
    main()
    
