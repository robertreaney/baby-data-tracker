import cv2
from pdf2image import convert_from_bytes, convert_from_path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def main(content, content_type):

    if content_type == 'application/pdf':
        images = convert_from_bytes(content)
    if content_type == 'image/jpeg':
        images = [Image.open(BytesIO(content))]
    else:
        raise ValueError(f'not yet supported content_type={content_type}')

    if len(images) > 1:
        raise ValueError(f'not yet supported len(images)={len(images)}')

    # Preprocessing
    image = np.array(images[0])
    # orig = image.copy()

    # convert to grayscale
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    (h, w) = image.shape
    new_h, new_w = (736, 736)
    r_H, r_W = (h / new_h, w / new_w)

    # resize image
    image = cv2.resize(image, (new_h, new_w))

    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    model = cv2.dnn_TextDetectionModel_DB('models/DB_IC15_resnet50.onnx')

    model.setInputParams(
        1.0 / 255.0,
        size = (new_h, new_w),
        mean = (122.67891434, 116.66876762, 104.00698793)
    )

    bounding_boxes, confidences = model.detectTextRectangles(image)
    
    # Iterate through bounding boxes and draw them on the image
    # for ((x, y), (w, h), a) in bounding_boxes:
    for rotated_rect in bounding_boxes:

        # Convert the rotated rectangle to 4 points
        points = cv2.boxPoints(rotated_rect)
        points = np.int0(points)

        # Calculate the axis-aligned bounding box of the rotated rectangle
        (x, y, w, h) = cv2.boundingRect(points)

        # Define the rectangle's top-left and bottom-right points
        start_point = (x, y)
        end_point = (x + w, y + h)
        
        # Define the color of the rectangle (BGR format) and thickness
        color = (0, 255, 0)  # Green
        thickness = 2
        
        # Draw the rectangle on the original image
        cv2.rectangle(image, start_point, end_point, color, thickness)

    cv2.imwrite('detected.jpg', image)

    # model = cv2.dnn.readNet('models/DB_IC15_resnet50.onnx')
    # model = cv2.dnn.readNet('models/frozen_east_text_detection.pb')

    # blob = cv2.dnn.blobFromImage(
    #     image, 
    #     scalefactor = 1.0 / 255.0,
    #     size = (new_w, new_h),
    #     mean = (122.67891434, 116.66876762, 104.00698793), 
    #     swapRB = True,
    #     crop = False
    # )

    # model.setInput(blob)
    # output = model.forward()

    # output.shape
    # cv2.imwrite('results.jpg', results)


    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                            cv2.THRESH_BINARY, 11, 2)
    # edges = cv2.Canny(blurred, 50, 150)
    # contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contour_image = image.copy()
    # cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

    # cv2.imwrite('cv_output_full_test.jpg', thresh)
    # cv2.imwrite('cv_edges_test.jpg', contour_image)


    # temp = cv2.resize(thresh, (736,1280))
    # cv2.imwrite('resize.jpg', temp)

    # text detection with DB_TD500_resnet50.onnx
    # model = cv2.dnn.readNet('models/DB_IC15_resnet50.onnx')
    # omodel = onnx.load('models/DB_IC15_resnet50.onnx')

    # processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    # model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")





if __name__ == '__main__':
    main('/home/ubuntu/projects/margot-data/src/ocr/tests/example_input.pdf', 'application/pdf')