import cv2
import supervision as sv
from ultralytics import YOLO


def main():
    # define resolution
    # cap = cv2.VideoCapture('rtsp://192.168.0.176:8080/h264_pcm.sdp')
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    # specify the model
    model = YOLO("train_v1.3.pt")
    class_names = {
        0: "caixa_fone",
        1: "controle_xbox",
        2: "garrafa",
        3: "mouse",
        4: "talco",
    }

    # customize the bounding box
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    while True:
        ret, frame = cap.read()
        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        labels = [
            f"{class_names[detections.class_id[0]]} {detections.confidence[0]:.2f}"
            for _, confidence, class_id, a
            in detections.xyxy
        ]
        if len(detections.class_id) == 0:
            pass
        else:
            if detections.confidence[0] > 0.8:
                frame = box_annotator.annotate(
                    scene=frame,
                    detections=detections,
                    labels=labels
                )

        cv2.imshow("yolov8", frame)

        if cv2.waitKey(30) == 27:  # break with escape key
            break

    cap.release()
    # writer.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
