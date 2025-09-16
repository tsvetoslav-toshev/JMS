import barcode
from barcode.writer import ImageWriter
from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import random
import logging
import sys
import os

# Set up logger first
logger = logging.getLogger(__name__)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
            logger.debug(f"PyInstaller mode: base_path = {base_path}")
        else:
            base_path = os.path.abspath(".")
            logger.debug(f"Development mode: base_path = {base_path}")
        
        full_path = os.path.join(base_path, relative_path)
        logger.debug(f"Trying resource path: {full_path}")
        
        # Check if file exists, if not try alternative paths
        if os.path.exists(full_path):
            logger.debug(f"Found resource at: {full_path}")
            return full_path
        
        # Try relative to script directory (development mode)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alt_path = os.path.join(script_dir, "..", relative_path)
        alt_path = os.path.normpath(alt_path)
        logger.debug(f"Trying alternative path: {alt_path}")
        
        if os.path.exists(alt_path):
            logger.debug(f"Found resource at alternative path: {alt_path}")
            return alt_path
        
        # Try current working directory
        cwd_path = os.path.join(os.getcwd(), relative_path)
        logger.debug(f"Trying current working directory path: {cwd_path}")
        
        if os.path.exists(cwd_path):
            logger.debug(f"Found resource in current working directory: {cwd_path}")
            return cwd_path
            
        # Last resort: return the original path and log warning
        logger.warning(f"Resource not found in any location: {relative_path}")
        logger.warning(f"Tried paths: {full_path}, {alt_path}, {cwd_path}")
        return full_path
        
    except Exception as e:
        logger.error(f"Error in resource_path for {relative_path}: {e}")
        return relative_path


class BarcodeGenerator:
    def __init__(self, output_dir="resources/barcodes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.barcode_dir = "barcodes"
        os.makedirs(self.barcode_dir, exist_ok=True)
        
        # Barcode label dimensions (in mm)
        self.label_width = 100  # mm
        self.label_height = 50  # mm
        self.barcode_height = 30  # mm
        self.text_height = 10  # mm
        self.margin = 5  # mm
        
        # Convert mm to pixels (assuming 300 DPI)
        self.dpi = 300
        self.mm_to_pixels = self.dpi / 25.4  # 25.4 mm in an inch
        
        # Calculate pixel dimensions
        self.label_width_px = int(self.label_width * self.mm_to_pixels)
        self.label_height_px = int(self.label_height * self.mm_to_pixels)
        self.barcode_height_px = int(self.barcode_height * self.mm_to_pixels)
        self.text_height_px = int(self.text_height * self.mm_to_pixels)
        self.margin_px = int(self.margin * self.mm_to_pixels)

    def generate_new_barcode(self):
        """Generate a new Code 128 barcode"""
        # Generate 7 random digits
        digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        # Return complete barcode (no check digit needed for Code 128)
        return digits

    def calculate_ean13_check_digit(self, code):
        """Calculate EAN-13 check digit"""
        total = 0
        for i, digit in enumerate(code):
            if i % 2 == 0:
                total += int(digit)
            else:
                total += int(digit) * 3
        check_digit = (10 - (total % 10)) % 10
        return check_digit

    def generate_barcode(self, code):
        """Generate barcode image for given code"""
        try:
            logger.debug(f"Generating barcode for code: {code}")
            logger.debug(f"Output directory: {self.output_dir}")
            
            # Ensure output directory exists and is writable
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Create Code 128 barcode with specific ImageWriter configuration
            from barcode import Code128
            logger.debug("Creating Code128 instance...")
            
            # Get the bundled font path
            font_path = resource_path('fonts/arial.ttf')
            logger.debug(f"Using font path for barcode: {font_path}")
            
            # Configure ImageWriter to use our bundled font
            writer_options = {
                'module_width': 0.2,
                'module_height': 15.0,
                'quiet_zone': 6.5,
                'font_size': 10,
                'text_distance': 5.0,
                'background': 'white',
                'foreground': 'black',
                'font_path': font_path,  # Specify our bundled font
                'write_text': True,
            }
            
            writer = ImageWriter()
            writer.set_options(writer_options)
            
            code128 = Code128(code, writer=writer)
            
            # Save to file
            filename = self.output_dir / f"{code}"
            logger.debug(f"Saving barcode to: {filename}")
            
            # Try to save the barcode
            result = code128.save(filename)
            logger.debug(f"Save result: {result}")
            
            # Check if file was created
            png_file = str(filename) + ".png"
            if os.path.exists(png_file):
                logger.debug(f"Barcode file created successfully: {png_file}")
                return str(filename)
            else:
                logger.error(f"Barcode file was not created at: {png_file}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating barcode: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
            # Fallback: try without text
            try:
                logger.info("Trying fallback barcode generation without text...")
                writer_options_fallback = {
                    'write_text': False,
                    'module_width': 0.2,
                    'module_height': 15.0,
                    'quiet_zone': 6.5,
                    'background': 'white',
                    'foreground': 'black',
                }
                
                writer = ImageWriter()
                writer.set_options(writer_options_fallback)
                code128 = Code128(code, writer=writer)
                
                filename = self.output_dir / f"{code}"
                result = code128.save(filename)
                
                png_file = str(filename) + ".png"
                if os.path.exists(png_file):
                    logger.info(f"Fallback barcode created successfully: {png_file}")
                    return str(filename)
                else:
                    logger.error(f"Fallback barcode also failed")
                    return None
                    
            except Exception as fallback_e:
                logger.error(f"Fallback barcode generation also failed: {fallback_e}")
                return None

    def _add_info_to_barcode(self, barcode_path, price=None, include_date=False):
        """Add price and/or date to barcode image"""
        try:
            # Open the barcode image
            img = Image.open(f"{barcode_path}.png")
            
            # Create a new image with white background
            new_img = Image.new('RGB', (self.label_width_px, self.label_height_px), 'white')
            draw = ImageDraw.Draw(new_img)
            
            # Calculate positions
            barcode_x = (self.label_width_px - img.width) // 2
            barcode_y = self.margin_px
            
            # Paste barcode
            new_img.paste(img, (barcode_x, barcode_y))
            
            # Add text below barcode
            text_y = barcode_y + self.barcode_height_px + self.margin_px
            
            # Try to load a font, fall back to default if not available
            # Load font for text
            font = None
            font_size = max(12, int(self.text_height_px * 0.8))
            
            # Try multiple font paths
            font_paths = [
                resource_path(os.path.join("fonts", "arial.ttf")),
                os.path.join("fonts", "arial.ttf"),
                "arial.ttf",
                r"C:\Windows\Fonts\arial.ttf",  # Windows system font
                r"C:\Windows\Fonts\Arial.ttf",  # Alternative name
            ]
            
            for font_path in font_paths:
                try:
                    if os.path.exists(font_path):
                        font = ImageFont.truetype(font_path, font_size)
                        logger.debug(f"Successfully loaded font from: {font_path}")
                        break
                except Exception as e:
                    logger.debug(f"Could not load font from {font_path}: {e}")
                    continue
            
            # If no TrueType font worked, use default
            if font is None:
                try:
                    font = ImageFont.load_default()
                    logger.warning("Using default font - TrueType fonts not available")
                except Exception as e:
                    logger.error(f"Could not load any font: {e}")
                    # Create a minimal font fallback
                    font = None
            
            # Add price if provided
            if price is not None:
                price_text = f"Цена: {self.format_number_with_spaces(price)} лв."
                try:
                    if font:
                        # Center the price text
                        text_width = draw.textlength(price_text, font=font)
                        text_x = (self.label_width_px - text_width) // 2
                        draw.text((text_x, text_y), price_text, fill='black', font=font)
                    else:
                        # Fallback without font
                        draw.text((self.margin_px, text_y), price_text, fill='black')
                    text_y += self.text_height_px
                except Exception as e:
                    logger.error(f"Error drawing price text: {e}")
            
            # Add date if requested
            if include_date:
                date_text = datetime.now().strftime("%d/%m/%Y")
                try:
                    if font:
                        # Center the date text
                        text_width = draw.textlength(date_text, font=font)
                        text_x = (self.label_width_px - text_width) // 2
                        draw.text((text_x, text_y), date_text, fill='black', font=font)
                    else:
                        # Fallback without font
                        draw.text((self.margin_px, text_y), date_text, fill='black')
                except Exception as e:
                    logger.error(f"Error drawing date text: {e}")
            
            # Save the modified image
            new_img.save(f"{barcode_path}.png")
        except Exception as e:
            logger.error(f"Error adding info to barcode: {str(e)}")
            
    def format_number_with_spaces(self, number):
        """Format number with spaces every 3 digits"""
        if isinstance(number, float):
            # Split into integer and decimal parts
            int_part, dec_part = str(number).split('.')
            # Format integer part with spaces
            formatted_int = ' '.join(int_part[i:i+3] for i in range(0, len(int_part), 3))
            return f"{formatted_int}.{dec_part}"
        else:
            # Format integer with spaces
            return ' '.join(str(number)[i:i+3] for i in range(0, len(str(number)), 3))
            
    def generate_qr_code(self, data):
        """Generate a QR code for the given data."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code
            output_path = self.output_dir / f"qr_{data}"
            img.save(f"{output_path}.png")
            
            return str(output_path) + ".png"
        except Exception as e:
            logger.error(f"Error generating QR code: {e}")
            return None

    def print_barcode(self, code):
        """Print barcode label"""
        try:
            # Generate barcode image
            barcode_path = self.generate_barcode(code)
            if barcode_path:
                # Printing functionality implemented in main.py PrinterHandler
                # For now, just return success
                return True
            return False
        except Exception as e:
            logger.error(f"Error printing barcode: {e}")
            return False
            
    def calculate_check_digit(self, code):
        """Calculate EAN13 check digit"""
        try:
            # Ensure code is 12 digits
            code = code.zfill(12)
            
            # Calculate check digit
            total = 0
            for i, digit in enumerate(code):
                if i % 2 == 0:
                    total += int(digit)
                else:
                    total += int(digit) * 3
                    
            check_digit = (10 - (total % 10)) % 10
            return str(check_digit)
        except Exception as e:
            logger.error(f"Error calculating check digit: {str(e)}")
            return None 