import cv2
from pyzbar.pyzbar import decode
import numpy as np
from PIL import Image
import logging

class BarcodeScanner:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Setup logging for barcode scanning operations"""
        self.logger = logging.getLogger('barcode_scanner')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('logs/barcode_scanner.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def scan_from_image(self, image_path):
        """Scan barcode from image file"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                self.logger.error(f"Failed to read image: {image_path}")
                return None

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply thresholding
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Find barcodes
            barcodes = decode(thresh)

            if barcodes:
                # Get the first barcode
                barcode = barcodes[0]
                barcode_data = barcode.data.decode('utf-8')
                self.logger.info(f"Found barcode: {barcode_data}")
                return barcode_data
            else:
                self.logger.warning("No barcode found in image")
                return None

        except Exception as e:
            self.logger.error(f"Error scanning barcode: {str(e)}")
            return None

    def scan_from_camera(self):
        """Scan barcode from camera feed"""
        try:
            # Initialize camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.logger.error("Failed to open camera")
                return None

            while True:
                # Read frame
                ret, frame = cap.read()
                if not ret:
                    self.logger.error("Failed to read frame")
                    break

                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Apply thresholding
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Find barcodes
                barcodes = decode(thresh)

                # Draw rectangle around barcode
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    barcode_data = barcode.data.decode('utf-8')
                    cv2.putText(frame, barcode_data, (x, y - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Show frame
                cv2.imshow('Barcode Scanner', frame)

                # Check for barcode
                if barcodes:
                    barcode_data = barcodes[0].data.decode('utf-8')
                    self.logger.info(f"Found barcode: {barcode_data}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return barcode_data

                # Check for exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            return None

        except Exception as e:
            self.logger.error(f"Error scanning barcode: {str(e)}")
            return None

    def generate_barcode(self, data, output_path):
        """Generate barcode image"""
        try:
            from barcode import Code128
            from barcode.writer import ImageWriter
            from utils.barcode import resource_path

            # Get font path for barcode text - use resource_path for PyInstaller compatibility
            barcode_font_path = resource_path("fonts/arial.ttf")

            # Generate barcode with bundled font
            writer = ImageWriter()
            barcode = Code128(data, writer=writer)
            
            # Use options to specify the bundled font
            barcode_options = {
                'font_path': barcode_font_path
            }
            
            barcode.save(output_path, options=barcode_options)

            self.logger.info(f"Generated barcode: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error generating barcode: {str(e)}")
            return False 