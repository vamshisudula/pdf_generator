import os
import pdfkit
from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
import io
import re
import importlib.util
import sys
import shutil

def natural_sort_key(s):
    """Sort strings that contain numbers in a natural way."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def load_content_data():
    """Load the content data from content_data.py"""
    try:
        # Get the directory of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        content_data_path = os.path.join(base_dir, "content_data.py")
        
        # Check if the content_data.py file exists
        if not os.path.exists(content_data_path):
            print("Warning: content_data.py not found. Dynamic content will not be available.")
            return {}
        
        # Dynamically import the content_data module
        spec = importlib.util.spec_from_file_location("content_data", content_data_path)
        content_data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(content_data)
        
        # Return the content mapping dictionary
        if hasattr(content_data, 'content_mapping'):
            return content_data.content_mapping
        else:
            print("Warning: content_mapping not found in content_data.py")
            return {}
    except Exception as e:
        print(f"Error loading content data: {e}")
        return {}

def create_temp_html_with_absolute_css_paths(html_file):
    """Create a temporary HTML file with absolute paths to CSS files and page-filling styling"""
    try:
        base_dir = os.path.dirname(os.path.abspath(html_file))
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace relative CSS paths with absolute paths
        content = content.replace('href="globals.css"', f'href="{os.path.join(base_dir, "globals.css")}"')
        content = content.replace('href="mutual_fund_style.css"', f'href="{os.path.join(base_dir, "mutual_fund_style.css")}"')
        content = content.replace('href="style.css"', f'href="{os.path.join(base_dir, "style.css")}"')
        
        # Replace dynamic content placeholders
        content_mapping = load_content_data()
        file_name = os.path.basename(html_file)
        
        if file_name in content_mapping:
            # Replace template variables with actual content
            dynamic_content = content_mapping[file_name]
            
            # Process the dynamic content to create proper HTML paragraphs
            if dynamic_content:
                # Split the content by double newlines to create paragraphs
                paragraphs = dynamic_content.strip().split('\n\n')
                formatted_content = ''
                for paragraph in paragraphs:
                    # Replace single newlines with spaces within paragraphs
                    paragraph = paragraph.replace('\n', ' ').strip()
                    if paragraph:
                        formatted_content += f'<p>{paragraph}</p>\n'
            
            # Direct variable replacements for asset allocation page
            if file_name == '5_asset_allocation.html':
                # Load all variables from content_data module
                content_data_module = sys.modules.get('content_data')
                
                # Use BeautifulSoup to parse and modify the HTML
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Update elements by ID
                    if hasattr(content_data_module, 'equity_percentage'):
                        element = soup.find(id='equity-percentage')
                        if element:
                            element.string = str(content_data_module.equity_percentage)
                    
                    if hasattr(content_data_module, 'debt_percentage'):
                        element = soup.find(id='debt-percentage')
                        if element:
                            element.string = str(content_data_module.debt_percentage)
                    
                    if hasattr(content_data_module, 'total_amount'):
                        element = soup.find(id='total-amount')
                        if element:
                            element.string = str(content_data_module.total_amount)
                    
                    if hasattr(content_data_module, 'mutual_funds_breakdown'):
                        element = soup.find(id='mutual-funds-breakdown')
                        if element:
                            element.clear()
                            element.append(BeautifulSoup(str(content_data_module.mutual_funds_breakdown), 'html.parser'))
                    
                    if hasattr(content_data_module, 'mutual_funds_amount'):
                        element = soup.find(id='mutual-funds-amount')
                        if element:
                            element.string = str(content_data_module.mutual_funds_amount)
                    
                    if hasattr(content_data_module, 'pms_amount'):
                        element = soup.find(id='pms-amount')
                        if element:
                            element.string = str(content_data_module.pms_amount)
                    
                    if hasattr(content_data_module, 'private_equity_amount'):
                        element = soup.find(id='private-equity-amount')
                        if element:
                            element.string = str(content_data_module.private_equity_amount)
                    
                    if hasattr(content_data_module, 'debt_amount'):
                        element = soup.find(id='debt-amount')
                        if element:
                            element.string = str(content_data_module.debt_amount)
                    
                    # Convert back to string
                    content = str(soup)
                except ImportError:
                    print("BeautifulSoup not installed. Using direct string replacement instead.")
                    # Fallback to direct string replacement if BeautifulSoup is not available
                    if hasattr(content_data_module, 'equity_percentage'):
                        content = re.sub(r'<div class="text-wrapper-3" id="equity-percentage">[^<]*</div>', 
                                        f'<div class="text-wrapper-3" id="equity-percentage">{content_data_module.equity_percentage}</div>', content)
                    
                    if hasattr(content_data_module, 'debt_percentage'):
                        content = re.sub(r'<div class="text-wrapper-4" id="debt-percentage">[^<]*</div>', 
                                        f'<div class="text-wrapper-4" id="debt-percentage">{content_data_module.debt_percentage}</div>', content)
                    
                    if hasattr(content_data_module, 'total_amount'):
                        content = re.sub(r'<div class="text-wrapper-9" id="total-amount">[^<]*</div>', 
                                        f'<div class="text-wrapper-9" id="total-amount">{content_data_module.total_amount}</div>', content)
                    
                    if hasattr(content_data_module, 'mutual_funds_amount'):
                        content = re.sub(r'<div class="text-wrapper-17" id="mutual-funds-amount">[^<]*</div>', 
                                        f'<div class="text-wrapper-17" id="mutual-funds-amount">{content_data_module.mutual_funds_amount}</div>', content)
                    
                    if hasattr(content_data_module, 'pms_amount'):
                        content = re.sub(r'<div class="text-wrapper-19" id="pms-amount">[^<]*</div>', 
                                        f'<div class="text-wrapper-19" id="pms-amount">{content_data_module.pms_amount}</div>', content)
                    
                    if hasattr(content_data_module, 'private_equity_amount'):
                        content = re.sub(r'<div class="text-wrapper-22" id="private-equity-amount">[^<]*</div>', 
                                        f'<div class="text-wrapper-22" id="private-equity-amount">{content_data_module.private_equity_amount}</div>', content)
                    
                    if hasattr(content_data_module, 'debt_amount'):
                        content = re.sub(r'<div class="text-wrapper-25" id="debt-amount">[^<]*</div>', 
                                        f'<div class="text-wrapper-25" id="debt-amount">{content_data_module.debt_amount}</div>', content)
                    
                    if hasattr(content_data_module, 'mutual_funds_breakdown'):
                        content = re.sub(r'<p class="large-cap-fund" id="mutual-funds-breakdown">.*?</p>', 
                                        f'<p class="large-cap-fund" id="mutual-funds-breakdown">{content_data_module.mutual_funds_breakdown}</p>', 
                                        content, flags=re.DOTALL)
            
            # Replace textarea content with formatted content
            if '{{textareaContent}}' in content:
                content = content.replace('{{textareaContent}}', formatted_content)
            
            # Handle other potential template variables
            # Example: <%= variableName %> pattern
            template_vars = re.findall(r'<%=\s*([\w_]+)\s*%>', content)
            for var in template_vars:
                if hasattr(sys.modules.get('content_data'), var):
                    var_content = getattr(sys.modules.get('content_data'), var)
                    content = content.replace(f'<%= {var} %>', str(var_content))
            
            # Handle double curly braces template format
            # Example: {{variableName}} pattern
            curly_template_vars = re.findall(r'\{\{([\w_]+)\}\}', content)
            for var in curly_template_vars:
                if hasattr(sys.modules.get('content_data'), var):
                    var_content = getattr(sys.modules.get('content_data'), var)
                    content = content.replace(f'{{{{{var}}}}}', str(var_content))
        
        # Add simple CSS to ensure all elements are visible
        additional_style = '''
<style>
@page {
  size: A4;
  margin: 0;
}

html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  position: relative;
}

/* Make all text elements visible */
p, div, span {
  display: block !important;
  visibility: visible !important;
}

/* Ensure all images are displayed */
img {
  max-width: 100%;
}

/* Increase font size slightly */
body {
  font-size: 110%;
}

/* Hide textarea elements in the output */
textarea {
  border: none;
  background: transparent;
  resize: none;
  overflow: hidden;
  font-family: inherit;
  font-size: inherit;
  color: inherit;
  line-height: inherit;
  padding: 0;
  margin: 0;
  width: 100%;
}
</style>'''
        
        if '<head>' in content:
            content = content.replace('<head>', '<head>' + additional_style)
        else:
            content = '<!DOCTYPE html><html><head>' + additional_style + '</head><body>' + content + '</body></html>'
            
        # Create a temporary file
        temp_file = os.path.join(os.path.dirname(html_file), f"temp_{os.path.basename(html_file)}")
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return temp_file
    except Exception as e:
        print(f"Error creating temporary HTML file: {e}")
        return None

def convert_html_to_pdf(html_file, output_pdf):
    """Convert HTML file to PDF with improved layout settings"""
    try:
        # Get the directory of the HTML file to set as base path for CSS files
        base_dir = os.path.dirname(os.path.abspath(html_file))
        
        # Simplified but effective configuration for wkhtmltopdf
        options = {
            'page-size': 'A4',
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            'quiet': '',
            # Key parameters for better rendering
            'javascript-delay': '2000',  # Increased delay to ensure JavaScript executes
            'no-stop-slow-scripts': None,
            'load-error-handling': 'ignore',
            'enable-external-links': None,
            'enable-internal-links': None,
            'disable-smart-shrinking': None,
            'zoom': '1.33',  # Scale content to reduce empty space
            'dpi': '300',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'background': None,
            'print-media-type': None,
            'enable-javascript': None,  # Explicitly enable JavaScript
            'run-script': "document.addEventListener('DOMContentLoaded', function() { console.log('DOM fully loaded'); });"
        }
        
        # Create a temporary HTML file with enhanced CSS
        temp_html = create_temp_html_with_absolute_css_paths(html_file)
        if temp_html:
            print(f"Converting {html_file} to PDF")
            pdfkit.from_file(temp_html, output_pdf, options=options)
            # Clean up temp file
            os.remove(temp_html)
        else:
            # Fall back to original file if temp creation failed
            pdfkit.from_file(html_file, output_pdf, options=options)
        
        return True
    except Exception as e:
        print(f"Error converting {html_file} to PDF: {e}")
        return False

def convert_image_to_pdf(image_file, output_pdf):
    """Convert image file to PDF with A4 size"""
    try:
        image = Image.open(image_file)
        
        # Convert to RGB if necessary (needed for some image types)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # A4 size in points (1 pt = 1/72 inch)
        a4_width_pt = 595
        a4_height_pt = 842
        
        # Calculate new image dimensions (preserving aspect ratio) to fit A4
        img_width, img_height = image.size
        width_ratio = a4_width_pt / img_width
        height_ratio = a4_height_pt / img_height
        
        # Use the smaller ratio to ensure the whole image fits on the page
        ratio = min(width_ratio, height_ratio)
        
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        # Resize image
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Create a white A4 background
        a4_img = Image.new('RGB', (a4_width_pt, a4_height_pt), (255, 255, 255))
        
        # Paste the resized image centered on the A4 canvas
        x_offset = (a4_width_pt - new_width) // 2
        y_offset = (a4_height_pt - new_height) // 2
        a4_img.paste(image, (x_offset, y_offset))
            
        # Save as PDF with A4 dimensions
        a4_img.save(output_pdf, "PDF", resolution=300.0)
        return True
    except Exception as e:
        print(f"Error converting {image_file} to PDF: {e}")
        return False

def merge_pdfs(pdf_files, output_file):
    """Merge multiple PDFs into a single PDF"""
    try:
        # Create a copy of the pdf_files list to avoid modifying the original
        pdf_files_to_merge = pdf_files.copy()
        
        pdf_writer = PdfWriter()
        
        for pdf_file in pdf_files_to_merge:
            if os.path.exists(pdf_file):
                print(f"Adding to merged PDF: {pdf_file}")
                pdf_reader = PdfReader(pdf_file)
                for page in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page])
            else:
                print(f"PDF file does not exist: {pdf_file}")
        
        # Write the merged PDF to the output file
        with open(output_file, 'wb') as out:
            pdf_writer.write(out)
        
        return True
    except Exception as e:
        print(f"Error merging PDFs: {e}")
        return False

def load_content_data_module():
    """Load the content_data.py module dynamically"""
    try:
        # Get the base directory of the script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        content_data_path = os.path.join(base_dir, "content_data.py")
        
        # Check if the content_data.py file exists
        if not os.path.exists(content_data_path):
            print("Warning: content_data.py not found. Cannot update HTML files.")
            return None
        
        # Dynamically import the content_data module
        spec = importlib.util.spec_from_file_location("content_data", content_data_path)
        content_data_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(content_data_module)
        
        return content_data_module
    except Exception as e:
        print(f"Error loading content data module: {e}")
        return None

def create_backup_if_needed(html_file):
    """Create a backup of the HTML file if it doesn't exist"""
    try:
        backup_file = f"{html_file}_original"
        if not os.path.exists(backup_file):
            shutil.copy2(html_file, backup_file)
            print(f"Created backup of HTML file at {backup_file}")
        return backup_file
    except Exception as e:
        print(f"Error creating backup file: {e}")
        return None

def update_asset_allocation_html():
    """Update the asset allocation HTML file with dynamic content"""
    try:
        # Load content data module
        content_data_module = load_content_data_module()
        if not content_data_module:
            return False
        
        # Get file paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(base_dir, "5_asset_allocation.html")
        backup_file = create_backup_if_needed(html_file)
        if not backup_file:
            return False
        
        # Read the original HTML file
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the content with dynamic values
        if hasattr(content_data_module, 'equity_percentage'):
            # Update the equity percentage text
            content = re.sub(r'<div class="text-wrapper-3"[^>]*>[^<]*</div>', 
                            f'<div class="text-wrapper-3" id="equity-percentage">{content_data_module.equity_percentage}</div>', content)
            
            # Update the bar chart width based on equity percentage
            equity_percent = int(content_data_module.equity_percentage.replace('%', ''))
            # Calculate the width in pixels (556px is the total width of the bar)
            equity_width = int(556 * equity_percent / 100)
            
            # Update the rectangle-2 div width which represents the equity portion of the bar
            content = re.sub(r'<div class="rectangle-2"[^>]*></div>', 
                            f'<div class="rectangle-2" style="width: {equity_width}px;"></div>', content)
        
        if hasattr(content_data_module, 'debt_percentage'):
            content = re.sub(r'<div class="text-wrapper-4"[^>]*>[^<]*</div>', 
                            f'<div class="text-wrapper-4" id="debt-percentage">{content_data_module.debt_percentage}</div>', content)
        
        if hasattr(content_data_module, 'total_amount'):
            content = re.sub(r'<div class="text-wrapper-9"[^>]*>[^<]*</div>', 
                            f'<div class="text-wrapper-9" id="total-amount">{content_data_module.total_amount}</div>', content)
        
        if hasattr(content_data_module, 'mutual_funds_breakdown'):
            content = re.sub(r'<p class="large-cap-fund"[^>]*>.*?</p>', 
                            f'<p class="large-cap-fund" id="mutual-funds-breakdown">{content_data_module.mutual_funds_breakdown}</p>', 
                            content, flags=re.DOTALL)
        
        if hasattr(content_data_module, 'mutual_funds_amount'):
            content = re.sub(r'<div class="text-wrapper-17"[^>]*>[^<]*</div>', 
                            f'<div class="text-wrapper-17" id="mutual-funds-amount">{content_data_module.mutual_funds_amount}</div>', content)
        
        if hasattr(content_data_module, 'pms_amount'):
            content = re.sub(r'<div class="text-wrapper-19"[^>]*>[^<]*</div>', 
                            f'<div class="text-wrapper-19" id="pms-amount">{content_data_module.pms_amount}</div>', content)
        
        if hasattr(content_data_module, 'private_equity_amount'):
            content = re.sub(r'<div class="text-wrapper-22"[^>]*>[^<]*</div>', 
                            f'<div class="text-wrapper-22" id="private-equity-amount">{content_data_module.private_equity_amount}</div>', content)
        
        if hasattr(content_data_module, 'debt_amount'):
            content = re.sub(r'<div class="text-wrapper-25"[^>]*>[^<]*</div>', 
                            f'<div class="text-wrapper-25" id="debt-amount">{content_data_module.debt_amount}</div>', content)
        
        # Write the updated content to the HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated asset allocation HTML with dynamic content")
        return True
    except Exception as e:
        print(f"Error updating asset allocation HTML: {e}")
        return False

def update_mutual_fund_html():
    """Update the mutual fund HTML file with dynamic content"""
    try:
        # Load content data module
        content_data_module = load_content_data_module()
        if not content_data_module:
            return False
        
        # Get file paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(base_dir, "6_mutual_fund.html")
        backup_file = create_backup_if_needed(html_file)
        if not backup_file:
            return False
        
        # Read the original HTML file
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the content with dynamic values
        if hasattr(content_data_module, 'mutual_fund_names'):
            content = re.sub(r'<p class="HDFC-top-fund"[^>]*>.*?</p>', 
                            f'<p class="HDFC-top-fund" id="mutual-fund-names">{content_data_module.mutual_fund_names}</p>', 
                            content, flags=re.DOTALL)
        
        if hasattr(content_data_module, 'mutual_fund_categories'):
            content = re.sub(r'<p class="largecap-largecap"[^>]*>.*?</p>', 
                            f'<p class="largecap-largecap" id="mutual-fund-categories">{content_data_module.mutual_fund_categories}</p>', 
                            content, flags=re.DOTALL)
        
        if hasattr(content_data_module, 'mutual_fund_returns_1yr'):
            content = re.sub(r'<div class="text-wrapper-7"[^>]*>.*?</div>', 
                            f'<div class="text-wrapper-7" id="mutual-fund-returns-1yr">{content_data_module.mutual_fund_returns_1yr}</div>', 
                            content, flags=re.DOTALL)
        
        if hasattr(content_data_module, 'mutual_fund_returns_3yr'):
            content = re.sub(r'<div class="text-wrapper-8"[^>]*>.*?</div>', 
                            f'<div class="text-wrapper-8" id="mutual-fund-returns-3yr">{content_data_module.mutual_fund_returns_3yr}</div>', 
                            content, flags=re.DOTALL)
        
        if hasattr(content_data_module, 'mutual_fund_returns_5yr'):
            content = re.sub(r'<div class="text-wrapper-9"[^>]*>.*?</div>', 
                            f'<div class="text-wrapper-9" id="mutual-fund-returns-5yr">{content_data_module.mutual_fund_returns_5yr}</div>', 
                            content, flags=re.DOTALL)
        
        # Write the updated content to the HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated mutual fund HTML with dynamic content")
        return True
    except Exception as e:
        print(f"Error updating mutual fund HTML: {e}")
        return False

def update_pms_html():
    """Update the PMS HTML file with dynamic content"""
    try:
        # Load content data module
        content_data_module = load_content_data_module()
        if not content_data_module:
            return False
        
        # Get file paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(base_dir, "7_pms.html")
        backup_file = create_backup_if_needed(html_file)
        if not backup_file:
            return False
        
        # Read the original HTML file
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the content with dynamic values
        if hasattr(content_data_module, 'pms_names'):
            content = re.sub(r'<p class="HDFC-top-fund"[^>]*>.*?</p>', 
                            f'<p class="HDFC-top-fund" id="pms-names">{content_data_module.pms_names}</p>', 
                            content, flags=re.DOTALL)
        
        if hasattr(content_data_module, 'pms_categories'):
            content = re.sub(r'<p class="largecap-largecap"[^>]*>.*?</p>', 
                            f'<p class="largecap-largecap" style="left: 261px;" id="pms-categories">{content_data_module.pms_categories}</p>', 
                            content, flags=re.DOTALL)
        
        if hasattr(content_data_module, 'pms_amounts'):
            content = re.sub(r'<div class="text-wrapper-7"[^>]*>.*?</div>', 
                            f'<div class="text-wrapper-7" style="left: 450px;" id="pms-amounts">{content_data_module.pms_amounts}</div>', 
                            content, flags=re.DOTALL)
        
        if hasattr(content_data_module, 'pms_target'):
            content = re.sub(r'<div class="text-wrapper-15"[^>]*>.*?</div>', 
                            f'<div class="text-wrapper-15" id="pms-target">{content_data_module.pms_target}</div>', 
                            content, flags=re.DOTALL)
        
        # Write the updated content to the HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated PMS HTML with dynamic content")
        return True
    except Exception as e:
        print(f"Error updating PMS HTML: {e}")
        return False

def update_fixed_income_html():
    """Update the fixed income HTML file with dynamic content"""
    try:
        # Load content data module
        content_data_module = load_content_data_module()
        if not content_data_module:
            return False
        
        # Get file paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(base_dir, "8_fixed_income.html")
        backup_file = create_backup_if_needed(html_file)
        if not backup_file:
            return False
        
        # Read the original HTML file
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the content with dynamic values
        if hasattr(content_data_module, 'fixed_income_data'):
            # Find the tbody tag and replace its content
            content = re.sub(r'(<tbody id="fixed-income-data">).*?(</tbody>)', 
                            f'\1{content_data_module.fixed_income_data}\2', 
                            content, flags=re.DOTALL)
        
        # Write the updated content to the HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated fixed income HTML with dynamic content")
        return True
    except Exception as e:
        print(f"Error updating fixed income HTML: {e}")
        return False

def update_private_equity_html():
    """Update the private equity HTML file with dynamic content"""
    try:
        # Load content data module
        content_data_module = load_content_data_module()
        if not content_data_module:
            return False
        
        # Get file paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(base_dir, "9_private_equity.html")
        backup_file = create_backup_if_needed(html_file)
        if not backup_file:
            return False
        
        # Read the original HTML file
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the content with dynamic values
        if hasattr(content_data_module, 'private_equity_data'):
            # Find the tbody tag and replace its content
            content = re.sub(r'(<tbody id="private-equity-data">).*?(</tbody>)', 
                            f'\1{content_data_module.private_equity_data}\2', 
                            content, flags=re.DOTALL)
        
        # Write the updated content to the HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated private equity HTML with dynamic content")
        return True
    except Exception as e:
        print(f"Error updating private equity HTML: {e}")
        return False

def update_direct_equity_html():
    """Update the direct equity HTML file with dynamic content"""
    try:
        # Load content data module
        content_data_module = load_content_data_module()
        if not content_data_module:
            return False
        
        # Get file paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(base_dir, "10_direct_equity.html")
        backup_file = create_backup_if_needed(html_file)
        if not backup_file:
            return False
        
        # Read the original HTML file
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the content with dynamic values
        if hasattr(content_data_module, 'direct_equity_data'):
            # Find the tbody tag and replace its content
            content = re.sub(r'(<tbody id="direct-equity-data">).*?(</tbody>)', 
                            f'\1{content_data_module.direct_equity_data}\2', 
                            content, flags=re.DOTALL)
        
        # Write the updated content to the HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated direct equity HTML with dynamic content")
        return True
    except Exception as e:
        print(f"Error updating direct equity HTML: {e}")
        return False

def main():
    # Get the base directory of the script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Update HTML files with dynamic content
    update_asset_allocation_html()
    update_mutual_fund_html()
    update_pms_html()
    update_fixed_income_html()
    update_private_equity_html()
    update_direct_equity_html()
    
    # Create temporary directory for individual PDFs
    temp_dir = os.path.join(base_dir, "temp_pdfs")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Output file
    output_file = os.path.join(output_dir, "combined_investment_proposal.pdf")
    
    # List to hold all PDF files in order
    pdf_files = []
    
    # Print directory contents to debug
    static_pdfs_dir = os.path.join(base_dir, "static pdfs")
    print(f"Checking static PDFs directory: {static_pdfs_dir}")
    if os.path.exists(static_pdfs_dir):
        print("Directory exists, listing contents:")
        for file in os.listdir(static_pdfs_dir):
            print(f"  - {file}")
    else:
        print("Directory does not exist")
        os.makedirs(static_pdfs_dir, exist_ok=True)
        print(f"Created directory: {static_pdfs_dir}")
    
    # 1. First file: Cover.pdf (instead of Cover Page.png)
    cover_pdf = os.path.join(base_dir, "static pdfs", "Cover.pdf")
    print(f"Looking for cover PDF at: {cover_pdf}")
    if os.path.exists(cover_pdf):
        print(f"Found cover PDF: {cover_pdf}")
        pdf_files.append(cover_pdf)
    else:
        print(f"Cover PDF file does not exist: {cover_pdf}")
        # Fall back to using the image
        cover_image = os.path.join(base_dir, "images", "Cover Page.png")
        cover_temp_pdf = os.path.join(temp_dir, "cover_page.pdf")
        if os.path.exists(cover_image) and convert_image_to_pdf(cover_image, cover_temp_pdf):
            pdf_files.append(cover_temp_pdf)
            print(f"Using converted image instead: {cover_image}")
    
    # 2. Introduction HTML
    intro_html = os.path.join(base_dir, "introduction.html")
    intro_pdf = os.path.join(temp_dir, "introduction.pdf")
    if convert_html_to_pdf(intro_html, intro_pdf):
        pdf_files.append(intro_pdf)
    
    # 3. Second file: our_products.pdf (instead of 2.png)
    products_pdf = os.path.join(base_dir, "static pdfs", "our_products.pdf")
    print(f"Looking for products PDF at: {products_pdf}")
    if os.path.exists(products_pdf):
        print(f"Found products PDF: {products_pdf}")
        pdf_files.append(products_pdf)
    else:
        print(f"Products PDF file does not exist: {products_pdf}")
        # Fall back to using the image
        second_image = os.path.join(base_dir, "images", "2.png")
        second_pdf = os.path.join(temp_dir, "image_2.pdf")
        if os.path.exists(second_image) and convert_image_to_pdf(second_image, second_pdf):
            pdf_files.append(second_pdf)
            print(f"Using converted image instead: {second_image}")
    
    # 4. HTML files from 3_market_outlook.html to 10_direct_equity.html
    html_files = []
    for i in range(3, 11):
        if i == 3:
            html_file = os.path.join(base_dir, f"{i}_market_outlook.html")
        elif i == 4:
            html_file = os.path.join(base_dir, f"{i}_debt_overview.html")
        elif i == 5:
            html_file = os.path.join(base_dir, f"{i}_asset_allocation.html")
        elif i == 6:
            html_file = os.path.join(base_dir, f"{i}_mutual_fund.html")
        elif i == 7:
            html_file = os.path.join(base_dir, f"{i}_pms.html")
        elif i == 8:
            html_file = os.path.join(base_dir, f"{i}_fixed_income.html")
        elif i == 9:
            html_file = os.path.join(base_dir, f"{i}_private_equity.html")
        elif i == 10:
            html_file = os.path.join(base_dir, f"{i}_direct_equity.html")
        
        if os.path.exists(html_file):
            html_files.append(html_file)
        else:
            print(f"HTML file does not exist: {html_file}")
    
    # Convert all HTML files to PDFs
    for html_file in html_files:
        file_name = os.path.basename(html_file)
        pdf_file = os.path.join(temp_dir, file_name.replace(".html", ".pdf"))
        print(f"Converting {html_file} to PDF")
        if convert_html_to_pdf(html_file, pdf_file):
            pdf_files.append(pdf_file)
    
    # 5. Last file: disclamer.pdf (instead of 11.png)
    disclaimer_pdf = os.path.join(base_dir, "static pdfs", "disclamer.pdf")
    print(f"Looking for disclaimer PDF at: {disclaimer_pdf}")
    if os.path.exists(disclaimer_pdf):
        print(f"Found disclaimer PDF: {disclaimer_pdf}")
        pdf_files.append(disclaimer_pdf)
    else:
        print(f"Disclaimer PDF file does not exist: {disclaimer_pdf}")
        # Fall back to using the image if the PDF doesn't exist
        last_image = os.path.join(base_dir, "images", "11.png")
        last_pdf = os.path.join(temp_dir, "image_11.pdf")
        if os.path.exists(last_image) and convert_image_to_pdf(last_image, last_pdf):
            pdf_files.append(last_pdf)
            print(f"Using converted image instead: {last_image}")
    
    # Merge all PDFs
    if merge_pdfs(pdf_files, output_file):
        print(f"Successfully created PDF: {output_file}")
    else:
        print("Failed to create combined PDF")
    
    # Identify which PDFs are temporary and which are from the static folder
    temp_pdf_files = []
    static_pdf_files = []
    
    # Check each PDF file path
    for pdf_file in pdf_files:
        # If the file is in the temp directory, it's a temporary file
        if temp_dir in pdf_file:
            temp_pdf_files.append(pdf_file)
        # If the file is in the static pdfs directory, it's a static file
        elif "static pdfs" in pdf_file:
            static_pdf_files.append(pdf_file)
            print(f"Identified static PDF (will preserve): {pdf_file}")
        # Otherwise, it's some other file we don't want to delete
        else:
            print(f"Skipping cleanup for: {pdf_file}")
    
    # Only delete temporary PDFs
    print(f"Found {len(temp_pdf_files)} temporary files to clean up")
    for pdf_file in temp_pdf_files:
        if os.path.exists(pdf_file):
            try:
                os.remove(pdf_file)
                print(f"Removed temporary file: {pdf_file}")
            except Exception as e:
                print(f"Error removing temporary file {pdf_file}: {e}")
    
    # Keep static PDFs intact
    print(f"Preserved {len(static_pdf_files)} static PDF files")
    
    try:
        os.rmdir(temp_dir)
    except Exception as e:
        print(f"Error removing temporary directory: {e}")

if __name__ == "__main__":
    main()
