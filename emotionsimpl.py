"""
Simple Emotion Detection System using Face Detection
Detects faces and shows basic emotional analysis
"""

import cv2
import numpy as np

class SimpleEmotionDetector:
    def __init__(self):
        # Load OpenCV's built-in face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
        print("Face detector initialized successfully!")
    
    def detect_emotion(self, frame):
        """Detect faces and basic features"""
        # Convert to grayscale
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
            
            # Get face region
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            # Detect eyes
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            
            # Detect smile
            smiles = self.smile_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.8,
                minNeighbors=20,
                minSize=(25, 25)
            )
            
            # Simple emotion estimation based on features
            emotion = "Neutral"
            if len(smiles) > 0:
                emotion = "Happy 😊"
                color = (0, 255, 0)
            elif len(eyes) < 2:
                emotion = "Uncertain"
                color = (0, 165, 255)
            else:
                emotion = "Neutral 😐"
                color = (255, 255, 255)
            
            # Display emotion
            cv2.putText(frame, emotion, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            # Draw eyes
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
            
            # Draw smile indicator
            if len(smiles) > 0:
                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)
            
            # Display feature count
            info_y = y + h + 25
            cv2.putText(frame, f"Eyes detected: {len(eyes)}", (x, info_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Smile detected: {len(smiles) > 0}", (x, info_y + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display face count
        cv2.putText(frame, f"Faces: {len(faces)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        return frame
    
    def run(self):
        """Run the emotion detection on webcam"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            print("Make sure your camera is connected and not being used by another app")
            return
        
        print("\n" + "="*60)
        print("SIMPLE EMOTION DETECTION SYSTEM")
        print("="*60)
        print("Controls:")
        print("  - Press 'q' to quit")
        print("  - Press 's' to save screenshot")
        print("  - Press 'SPACE' to pause/unpause")
        print("="*60 + "\n")
        
        screenshot_count = 0
        paused = False
        
        while True:
            if not paused:
                ret, frame = cap.read()
                
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                # Detect emotions
                processed_frame = self.detect_emotion(frame)
            
            # Display the frame
            cv2.imshow('Emotion Detection - Press Q to Quit', processed_frame if not paused else frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                screenshot_count += 1
                filename = f'emotion_screenshot_{screenshot_count}.jpg'
                cv2.imwrite(filename, processed_frame if not paused else frame)
                print(f"Screenshot saved: {filename}")
            elif key == ord(' '):
                paused = not paused
                print("Paused" if paused else "Resumed")
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("\nEmotion detection stopped. Thank you!")

def main():
    """Main function"""
    print("Initializing Simple Emotion Detection System...")
    print("\nThis version uses OpenCV's built-in classifiers")
    print("It detects faces, eyes, and smiles to estimate basic emotions\n")
    
    try:
        detector = SimpleEmotionDetector()
        detector.run()
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Make sure your webcam is accessible")

if __name__ == "__main__":
    main()