import os
import requests

def download_pdfs(base_url, start_number, end_number, download_folder):
    """
    Download PDFs from a series of numbered URLs.
    
    Args:
    base_url (str): Base URL with a placeholder for the number
    start_number (int): Starting number to check
    end_number (int): Ending number to check
    download_folder (str): Folder to save downloaded PDFs
    """
    # Create download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    for number in range(start_number, end_number + 1):
        # Construct PDF URL
        pdf_url = base_url.replace('486.pdf', f'{number}.pdf')
        
        try:
            # Send a HEAD request to check PDF existence
            response = requests.head(pdf_url)
            
            # Check if the PDF exists (200 OK status)
            if response.status_code == 200:
                # Download the PDF
                pdf_response = requests.get(pdf_url)
                
                # Save the PDF
                pdf_path = os.path.join(download_folder, f'{number}.pdf')
                with open(pdf_path, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                
                print(f'Downloaded: {number}.pdf')
            else:
                print(f'PDF not found: {number}.pdf')
        
        except requests.RequestException as e:
            print(f'Error processing {number}.pdf: {e}')


base_url = 'https://legislativediv.portal.gov.bd/sites/default/files/files/legislativediv.portal.gov.bd/page/f6053f58_1c99_44b6_9821_b4481a56094c/486.pdf'
download_folder = './downloaded_pdfs'

# Download PDFs from 486 to 500
download_pdfs(base_url, 200, 1000, download_folder)