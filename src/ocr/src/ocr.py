import cv2
from pdf2image import convert_from_bytes, convert_from_path
import numpy as np
import matplotlib.pyplot as plt


def main(content, content_type):

    if content_type == 'application/pdf':
        images = convert_from_bytes(content)
    else:
        raise ValueError(f'not yet supported content_type={content_type}')

    if len(images) > 1:
        raise ValueError(f'not yet supported len(images)={len(images)}')
    
    print('x')

    # image = images[0]
    # image = np.array(image)

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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