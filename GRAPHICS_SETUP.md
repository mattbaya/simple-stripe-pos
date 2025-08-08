# Graphics Setup Guide

This document explains how to create and configure graphics for your POS system.

## Required Graphics

### 1. Organization Logo (`static/logo.png`)
- **Purpose**: Displayed on the web interface and success modal
- **Recommended Size**: 150x150 pixels (square format)
- **Format**: PNG with transparent background preferred
- **Usage**: Shows in top-left of payment interface

### 2. Email Letterhead (`templates/letterhead.png`)
- **Purpose**: Embedded at the top of email receipts
- **Recommended Size**: 800x200 pixels (landscape format)
- **Format**: PNG or JPG
- **Usage**: Professional header for donor acknowledgment emails

## Creating Your Graphics

### Option 1: Use Provided Examples
We provide SVG examples that you can customize:
- `static/example-logo.svg` - Generic community association logo
- `templates/example-letterhead.svg` - Generic letterhead template

### Option 2: Professional Design Services
Consider hiring a designer for professional branding:
- Fiverr, Upwork, or local design agencies
- Provide your organization name, colors, and any existing branding
- Request both web logo and email letterhead versions

### Option 3: DIY Tools
Free/low-cost design tools:
- **Canva**: Templates for logos and letterheads
- **GIMP**: Free image editing software
- **Inkscape**: Free vector graphics editor
- **Google Drawings**: Simple web-based tool

## Converting SVG to PNG

If you have SVG files, convert them to PNG for better email compatibility:

```bash
# Using ImageMagick (if available)
convert example-logo.svg -background transparent -resize 150x150 logo.png
convert example-letterhead.svg -background white -resize 800x200 letterhead.png

# Using Inkscape
inkscape --export-type=png --export-width=150 --export-height=150 example-logo.svg
inkscape --export-type=png --export-width=800 --export-height=200 example-letterhead.svg

# Online conversion
# Upload SVG files to online converters like:
# - cloudconvert.com
# - convertio.co
# - online-convert.com
```

## File Placement

Once you have your graphics:

1. **Logo**: Save as `static/logo.png`
2. **Letterhead**: Save as `templates/letterhead.png`
3. **Update Configuration**: 
   - Set `ORGANIZATION_LOGO=/static/logo.png` in your `.env` file
   - The letterhead is automatically used by the email template

## Testing Your Graphics

1. **Logo Test**: Visit your POS interface to see the logo display
2. **Letterhead Test**: Process a test donation to receive an email receipt
3. **Responsive Check**: Test on mobile and desktop devices

## Branding Consistency

Ensure your graphics match your organization's existing branding:
- Use consistent colors, fonts, and styling
- Include your organization's legal name
- Consider adding contact information to letterhead
- Maintain professional appearance for donor confidence

## File Size Optimization

Keep file sizes reasonable:
- **Logo**: Under 50KB
- **Letterhead**: Under 200KB
- Use PNG compression or JPG quality settings to balance size and quality

## Backup and Version Control

- Keep source files (SVG, design files) in a separate location
- Don't commit large image files to git (they're in .gitignore)
- Document any design specifications or brand guidelines