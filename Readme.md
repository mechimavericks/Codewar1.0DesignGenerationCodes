# Event ID Card Generator

An automated ID card generation system that creates personalized ID cards with QR codes from CSV data and converts them to PDF format for easy printing and distribution.

## Features

- **Automated ID Card Generation**: Creates individual ID cards from CSV participant data
- **QR Code Integration**: Generates QR codes linking to Google Forms with participant information
- **Template-based Design**: Uses custom card templates with font support
- **Batch Processing**: Processes multiple participants efficiently
- **PDF Conversion**: Converts generated cards to PDF format (individual or combined)
- **Error Handling**: Tracks and reports failed card generations

## Requirements

```bash
pip install pandas qrcode[pil] pillow reportlab
```

## File Structure

```
.
├── main.py              # Main ID card generation script
├── pdfConverter.py      # PDF conversion utilities
├── ParticipantList.csv  # Input CSV with participant data
├── card.png             # ID card template image
├── font.otf             # Custom font file
├── id_cards/            # Generated ID card images
└── individual_pdfs/     # Individual PDF files (optional)
```

## Usage

### 1. ID Card Generation

#### Prepare CSV File
Create a `ParticipantList.csv` with the following columns:
- `Full Name` or `name`
- `Email Address` or `email`
- `Faculty` or `faculty`

#### Run ID Card Generation
```bash
python main.py
```

This will:
- Read participant data from `ParticipantList.csv`
- Generate QR codes with Google Forms links
- Create individual ID cards using the template
- Save cards as PNG images in `id_cards/` folder
- Generate a `faileddata.txt` file for any failures

### 2. PDF Conversion

#### Combined PDF (All cards in one file)
```bash
python pdfConverter.py --mode combined --output event_cards.pdf
```

#### Individual PDFs (Separate PDF for each card)
```bash
python pdfConverter.py --mode individual
```

#### Both Combined and Individual PDFs
```bash
python pdfConverter.py --mode both
```

#### Custom Input Folder
```bash
python pdfConverter.py --input custom_folder --mode combined
```

## Configuration

### QR Code Data
The QR codes contain URLs to a Google Form with pre-filled participant information:
- Name
- Email
- Faculty

### Card Template
- Place your card template as `card.png` in the root directory
- Template should be in PNG format with RGBA support
- QR code will be centered on the card
- Name will appear below the QR code in white text

### Font Customization
- Place custom font file as `font.otf`
- Font size is set to 60px for name text
- Falls back to system fonts if custom font is unavailable

## Command Line Options

### pdfConverter.py Options
```bash
--mode          # PDF creation mode: combined, individual, or both
--input         # Input folder containing ID card images (default: id_cards)
--output        # Output PDF filename for combined mode (default: id_cards.pdf)
```

## Output Files

### Generated Files
- `id_cards/*.png` - Individual ID card images
- `id_cards.pdf` - Combined PDF (if generated)
- `individual_pdfs/*.pdf` - Individual PDF files (if generated)
- `faileddata.txt` - Log of failed card generations

### Error Handling
Failed card generations are logged with:
- Row number from CSV
- Participant information
- Failure reason

## Customization

### Template Modifications
To modify the card layout, edit the [`create_id_card`](main.py) function in [main.py](main.py):
- QR code position: Modify `qr_position` calculation
- Text position: Adjust `text_position` calculation
- Font size: Change the font size parameter
- Colors: Modify fill colors for text

### QR Code Content
To change QR code data format, modify the URL generation in [`create_id_card`](main.py):
```python
raw = f"https://your-form-url.com?param1={name}&param2={email}"
```

## Troubleshooting

### Common Issues

1. **Template not found**: Ensure `card.png` exists in the root directory
2. **Font not loading**: Check if `font.otf` exists or install system fonts
3. **CSV format issues**: Verify column names match expected formats
4. **Empty QR codes**: Check if participant data contains valid name/email

### PDF Generation Issues
- Ensure `id_cards/` folder exists and contains PNG files
- Check file permissions for output directories
- Verify PIL and reportlab are properly installed

## Example Usage

```bash
# Generate all ID cards from CSV
python main.py

# Create combined PDF
python pdfConverter.py --mode combined --output event_badges.pdf

# Create individual PDFs for each participant
python pdfConverter.py --mode individual

# Process custom image folder
python pdfConverter.py --input custom_cards --mode both
```

## License

This project is designed for event management and ID card generation purposes.