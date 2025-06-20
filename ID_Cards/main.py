import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import json
import urllib.parse

def create_transparent_qr(data):
    """Create a QR code with transparent background"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create QR with transparent background
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.convert('RGBA')
    
    # Make white pixels transparent
    data = qr_img.getdata()
    new_data = []
    for item in data:
        # Change white to transparent
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)  # Keep original color
    
    qr_img.putdata(new_data)
    return qr_img

def create_id_card(name, email, faculty):
    # Combine data for QR code
    # Split name into parts
    raw = "<URL GOES HERE FOR THE QR CODE>"
    # url encoder 
    data = urllib.parse.quote(raw, safe=':/?=&')


    # print(data)

    # Convert to JSON for QR code
    qr_data = json.dumps(data)
    
    # Generate transparent QR code
    qr_img = create_transparent_qr(qr_data)
    
    try:
        # Open the template image
        template = Image.open("card.png")
        template = template.convert('RGBA')
        
        # Get dimensions
        card_width, card_height = template.size
        
        # Resize QR code if needed (adjust size as needed)
        qr_size = min(card_width // 3, card_height // 2)  # Appropriate size for the template
        qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
        qr_width, qr_height = qr_img.size
        
        # Create white background for QR code with 5px padding
        qr_bg_size = (qr_width -1, qr_height -1)  # 5px padding on each side
        qr_bg = Image.new('RGBA', qr_bg_size, (255, 255, 255, 255))
        
        # Center the QR code on its b-1ackground
        qr_bg.paste(qr_img, qr_img)  # 5px from each edge
        
        # Center the QR code with background on the template
        qr_position = ((card_width - qr_bg_size[0]) // 2, (card_height - qr_bg_size[1]) // 2 - 20)
        
        # Paste QR code with white background and transparency preserved
        template.paste(qr_bg, qr_position, qr_bg)
        
        # Add name below QR code
        draw = ImageDraw.Draw(template)
        
        # Try to load a font, fall back to default if needed
        try:
            font = ImageFont.truetype("./font.otf", 60)  # Changed to 16px
        except IOError:
            print("Custom font not found, using system font.")
            try:
                font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", 60)  # Changed to 16px
            except IOError:
                try:
                    font = ImageFont.truetype("./font.otf", 60)  # Changed to 16px
                except IOError:
                    font = ImageFont.load_default()
        
        # Center the text below QR code
        name=name.upper()
        text_width = draw.textlength(name, font=font)
        # text_position = ((card_width - text_width) // 2, qr_position[1] + qr_bg_size[1] + 20)
        # text position need to be center horizontally and 20px below the QR code
        text_position = ((card_width - text_width) // 2, qr_position[1] + qr_bg_size[1] + 180)


        
        # Draw the name in white
        draw.text(text_position, name, fill="white", font=font)
        
    except FileNotFoundError:
        print(f"Warning: Template 'idcard.png' not found. Creating plain card.")
        # Fallback to plain white card if template not found
        card_width, card_height = 500, 300
        template = Image.new('RGBA', (card_width, card_height), color=(255, 255, 255, 255))
        
        # Get QR dimensions
        qr_width, qr_height = qr_img.size
        
        # Create white background for QR code with 5px padding
        qr_bg_size = (qr_width + 10, qr_height + 10)
        qr_bg = Image.new('RGBA', qr_bg_size, (255, 255, 255, 255))
        
        # Center the QR code on its background
        qr_bg.paste(qr_img, (5, 5), qr_img)
        
        # Center the QR code with background on the card
        qr_position = ((card_width - qr_bg_size[0]) // 2, (card_height - qr_bg_size[1]) // 2 - 20)
        
        # Paste QR code with background
        template.paste(qr_bg, qr_position)
        
        # Add name below QR code
        draw = ImageDraw.Draw(template)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Center the text below QR code (if font available)
        if font:
            text_width = draw.textlength(name, font=font)
            text_position = ((card_width - text_width) // 2, qr_position[1] + qr_bg_size[1] + 10)
            draw.text(text_position, name, fill="white", font=font)
    
    # Create directory for output if it doesn't exist
    os.makedirs("id_cards", exist_ok=True)
    
    # Save the ID card
    filename = f"id_cards/{name.replace(' ', '_')}_id_card.png"
    template.save(filename)
    print(f"Created ID card for {name} at {filename}")
    
    return filename

def main():
    try:
        # Read the CSV file
        excel_file = "ParticipantList.csv"  # Adjust filename if needed
        df = pd.read_csv(excel_file)
        
        print(f"Processing {len(df)} records from {excel_file}...")
        
        # Initialize lists to track success and failures
        failed_records = []
        successful_count = 0
        
        # Process each row in the CSV file
        for index, row in df.iterrows():
            try:
                # Get data, checking multiple possible column name formats
                name = row.get('Full Name', row.get('name', ''))
                email = row.get('Email Address', row.get('email', ''))
                faculty = str(row.get('Faculty', row.get('faculty', '')))
                
                # Only create card if there's a name and email
                if name and email:
                    create_id_card(name, email, faculty)
                    successful_count += 1
                else:
                    # Record missing data
                    failed_records.append({
                        'index': index + 1,
                        'name': name,
                        'email': email,
                        'faculty': faculty,
                        'reason': 'Missing name or email'
                    })
                
                # Progress indicator for large datasets
                if index > 0 and index % 10 == 0:
                    print(f"Processed {index} records...")
                
            except Exception as e:
                # Record failed creation
                failed_records.append({
                    'index': index + 1,
                    'name': row.get('Full Name', row.get('name', 'Unknown')),
                    'email': row.get('Email Address', row.get('email', 'Unknown')),
                    'faculty': str(row.get('Faculty', row.get('faculty', 'Unknown'))),
                    'reason': str(e)
                })
                print(f"Failed to create ID card for row {index + 1}: {e}")
            
            # Remove the break statement to process all records
            # break
        
        # Write failed records to file if any
        if failed_records:
            with open("faileddata.txt", "w") as f:
                f.write("FAILED ID CARD CREATION RECORDS\n")
                f.write("=" * 50 + "\n\n")
                for record in failed_records:
                    f.write(f"Row: {record['index']}\n")
                    f.write(f"Name: {record['name']}\n")
                    f.write(f"Email: {record['email']}\n")
                    f.write(f"Faculty: {record['faculty']}\n")
                    f.write(f"Reason: {record['reason']}\n")
                    f.write("-" * 30 + "\n")
            
            print(f"\n{len(failed_records)} records failed. Details saved to 'faileddata.txt'")
        
        print(f"\nSummary:")
        print(f"Successfully created: {successful_count} ID cards")
        print(f"Failed: {len(failed_records)} records")
        print("All ID cards processing completed!")
        
    except FileNotFoundError:
        print(f"Error: CSV file '{excel_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
