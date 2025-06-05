import os
from PIL import Image
import glob
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
import argparse

def images_to_pdf(image_folder="id_cards", output_pdf="id_cards.pdf", cards_per_page=1):
    """
    Convert ID card images to PDF format keeping exact original image size
    
    Args:
        image_folder (str): Folder containing ID card images
        output_pdf (str): Output PDF filename
        cards_per_page (int): Number of cards per page (default: 1 for full size)
    """
    
    # Check if the image folder exists
    if not os.path.exists(image_folder):
        print(f"Error: Image folder '{image_folder}' not found.")
        return False
    
    # Get all PNG images from the folder
    image_pattern = os.path.join(image_folder, "*.png")
    image_files = glob.glob(image_pattern)
    
    if not image_files:
        print(f"No PNG images found in '{image_folder}' folder.")
        return False
    
    # Sort images for consistent ordering
    image_files.sort()
    
    print(f"Found {len(image_files)} ID card images")
    print(f"Creating PDF with exact image sizes...")
    
    # Create PDF with first image dimensions
    first_img = Image.open(image_files[0])
    img_width, img_height = first_img.size
    
    # Create PDF with exact image size
    c = canvas.Canvas(output_pdf, pagesize=(img_width, img_height))
    
    for i, image_path in enumerate(image_files):
        try:
            # Open image
            img = Image.open(image_path)
            current_width, current_height = img.size
            
            # If image size is different from first image, create new page with that size
            if current_width != img_width or current_height != img_height:
                if i > 0:  # Save current page before creating new one
                    c.showPage()
                # Set new page size for this image
                c.setPageSize((current_width, current_height))
                img_width, img_height = current_width, current_height
            
            # Draw image at exact size starting from bottom-left corner (0,0)
            c.drawImage(image_path, 0, 0, width=img_width, height=img_height)
            
            # Start new page for next image (except for last image)
            if i < len(image_files) - 1:
                c.showPage()
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(image_files)} images...")
                
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            continue
    
    # Save PDF
    c.save()
    print(f"PDF created successfully: {output_pdf}")
    print(f"Total pages: {len(image_files)}")
    return True

def create_individual_pdfs(image_folder="id_cards", output_folder="individual_pdfs"):
    """
    Create individual PDF files for each ID card image with exact image size
    
    Args:
        image_folder (str): Folder containing ID card images
        output_folder (str): Output folder for individual PDFs
    """
    
    # Check if the image folder exists
    if not os.path.exists(image_folder):
        print(f"Error: Image folder '{image_folder}' not found.")
        return False
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all PNG images from the folder
    image_pattern = os.path.join(image_folder, "*.png")
    image_files = glob.glob(image_pattern)
    
    if not image_files:
        print(f"No PNG images found in '{image_folder}' folder.")
        return False
    
    print(f"Creating individual PDFs for {len(image_files)} ID cards...")
    
    successful_count = 0
    failed_count = 0
    
    for image_path in image_files:
        try:
            # Get filename without extension
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            pdf_filename = os.path.join(output_folder, f"{base_name}.pdf")
            
            # Open image to get exact dimensions
            img = Image.open(image_path)
            img_width, img_height = img.size
            
            # Create PDF with exact image size
            c = canvas.Canvas(pdf_filename, pagesize=(img_width, img_height))
            
            # Draw image at exact size
            c.drawImage(image_path, 0, 0, width=img_width, height=img_height)
            c.save()
            
            successful_count += 1
            
        except Exception as e:
            print(f"Error creating PDF for {image_path}: {e}")
            failed_count += 1
    
    print(f"Individual PDFs created: {successful_count} successful, {failed_count} failed")
    print(f"PDFs saved in '{output_folder}' folder")
    return True

def main():
    parser = argparse.ArgumentParser(description="Convert ID card images to PDF")
    parser.add_argument("--mode", choices=["combined", "individual", "both"], 
                       default="combined", help="PDF creation mode")
    parser.add_argument("--input", default="id_cards", 
                       help="Input folder containing images")
    parser.add_argument("--output", default="id_cards.pdf", 
                       help="Output PDF filename (for combined mode)")
    
    args = parser.parse_args()
    
    if args.mode in ["combined", "both"]:
        print("Creating combined PDF...")
        images_to_pdf(args.input, args.output)
    
    if args.mode in ["individual", "both"]:
        print("Creating individual PDFs...")
        create_individual_pdfs(args.input, "individual_pdfs")
    
    print("PDF conversion completed!")

if __name__ == "__main__":
    main()