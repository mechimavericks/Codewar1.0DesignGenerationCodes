import csv
import os
from PIL import Image, ImageDraw, ImageFont

def generate_certificates():
    # File paths
    csv_file = 'participantlist.csv'
    template_image = 'participant.png'
    output_folder = 'participants_certificates'
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Check if files exist
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return
    
    if not os.path.exists(template_image):
        print(f"Error: {template_image} not found!")
        return
    
    try:
        # Load the certificate template
        template = Image.open(template_image)
        template_width, template_height = template.size
        
        # Try to load Roboto font (you may need to adjust the path and size)
        try:
            # Common paths for Roboto font on Linux
            font_paths = [
                "./font.ttf",
            ]
            
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 60)  # Adjust size as needed
                    break
            
            if font is None:
                print("Roboto font not found, using default font")
                font = ImageFont.load_default()
                
        except Exception as e:
            print(f"Error loading font: {e}")
            font = ImageFont.load_default()
        
        # Read names from CSV file
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            # Skip header row if it exists
            header = next(csv_reader, None)
            if header and header[0].lower() in ['name']:
                pass  # Header skipped
            else:
                # If first row is not a header, process it as data
                file.seek(0)
                csv_reader = csv.reader(file)
            
            certificate_count = 0
            
            for row in csv_reader:
                if row and row[0].strip():  # Check if name exists and is not empty
                    name = row[0].strip()
                    
                    # Create a copy of the template
                    certificate = template.copy()
                    draw = ImageDraw.Draw(certificate)
                    
                    # Get text dimensions for centering
                    bbox = draw.textbbox((0, 0), name, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    # Calculate position to center the text
                    # Adjust these values based on where you want the name on your certificate
                    x = (template_width - text_width) // 2
                    y = (template_height - text_height) // 2  # Center vertically
                    
                    # You might want to adjust the y position based on your certificate design
                    # For example, if the name should be in the lower half:
                    # y = template_height * 0.6
                    
                    # Draw the name on the certificate
                    draw.text((x, y-5), name, fill='#333333', font=font)  # Adjust color as needed
                    
                    # Save the certificate
                    output_filename = f"{output_folder}/certificate_{name.replace(' ', '_')}.png"
                    certificate.save(output_filename)
                    
                    certificate_count += 1
                    print(f"Generated certificate for: {name}")
                    # break
            
            print(f"\nTotal certificates generated: {certificate_count}")
            print(f"Certificates saved in: {output_folder}")
    
    except FileNotFoundError:
        print(f"Error: {csv_file} not found!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    
    # Generate certificates
    generate_certificates()