import cv2
import os
from insightface.app import FaceAnalysis

def load_detector():
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app

def detect_and_show(app, image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image: {image_path}")
        return

    faces = app.get(img)
    print(f"{image_path}: {len(faces)} face(s) detected")

    for face in faces:
        box = face.bbox.astype(int)
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

    cv2.imshow("Detection Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app = load_detector()

    test_folder = os.path.join("dataset", "raw", "080BEI013")
    for filename in os.listdir(test_folder):
        image_path = os.path.join(test_folder, filename)
        detect_and_show(app, image_path)