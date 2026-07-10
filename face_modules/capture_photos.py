import cv2
import os

def capture_for_student(roll_number, num_photos=5):
    folder = os.path.join("dataset", "raw", roll_number)
    os.makedirs(folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    print(f"Capturing photos for {roll_number}")
    print("Press SPACE to capture, 'q' to quit early")

    while count < num_photos:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        cv2.putText(display, f"Captured: {count}/{num_photos}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Capture", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            filepath = os.path.join(folder, f"img{count+1}.jpg")
            cv2.imwrite(filepath, frame)
            print(f"Saved {filepath}")
            count += 1
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. {count} photos saved for {roll_number}")

if __name__ == "__main__":
    roll_number = input("Enter roll number: ").strip()
    capture_for_student(roll_number)