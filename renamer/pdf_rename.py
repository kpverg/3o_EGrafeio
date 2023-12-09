import fitz  # PyMuPDF
from PIL import Image
import pytesseract,os
from pdf2image import convert_from_path
import re,sys
import shutil

loadInitFilepath= os.path.abspath('renamer\\configuration')
sys.path.append(loadInitFilepath)
import pathmodules as pathmod
 
from datetime import datetime

# Get the current date and time
now = datetime.now()

# Extract year, month, and day
current_year = now.year
current_month = now.month
current_day = now.day
mistakes = {'Ο': '0',
                'O': '0',
                'Δ': '4',
                'a': '',
                'ἂ': '',
                'Ί': '1',
                'Β':'8'
                }

pattern_f = re.compile('(Φ\..{3}|Φ\..{3}\..{1,3})\s?/.*\s?/.*')
pattern_s = re.compile('Σ\..*')
pattern_date = re.compile(
    '[0-9]{1,2}\s*(Ιαν|Φεβ|Μαρ|Απρ|Μαι|Μαϊ|Ιουν|Ιούν|Ιουλ|Ιούλ|Αυγ|Σεπ|Οκτ|Νοε|Νοέ|Δεκ)\s*[0-9]{2,4}')

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
class DocumentsManager:
    def __init__(self):
        self.selectRootPath=pathmod.FolderPathManager()
        self.currentpath=self.selectRootPath.getsavedpath()
        self.newfolderpath=""
        self.osname=os.name
        self.process_pdfs_in_directory()
 


    def extract_and_ocr_half_page(self):
        try:
            pdf_document = fitz.open(self.pdf_path)
            first_page = pdf_document[0]

            # Calculate the dimensions for the first half of the page
            half_width = first_page.rect.width 
            half_height = first_page.rect.height/ 3

            # Create a new rectangle for the first half of the page
            half_rect = fitz.Rect(0, 0, half_width, half_height)

            # Extract a pixmap from the first half of the page
            half_pixmap = first_page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=half_rect)

            # Convert the pixmap to an image
            img = Image.frombytes("RGB", [half_pixmap.width, half_pixmap.height], half_pixmap.samples)

            # Perform OCR on the image
            self.text = pytesseract.image_to_string(img, lang='ell')  # Use 'eng+ell' for English and Greek
            # select_folder()
            self.thema=self.extractThemaFromDocument()
            
            self.cratefolderWithnameThema()
            self.removeDoc()
            self.renamepdfDoc()
            
            
            return self.text
        except Exception as e:
            #print(f"Error extracting and OCR from {pdf_path}: {e}")
            return None
        
        
        
    def removeDoc(self):
    # pdf_filename = os.path.basename(self.pdf_file)    
    # Build the new path for the PDF in the destination folder
        # destination_path = os.path.join(destination_folder, self.pdf_file)
        if os.name == 'nt':
            self.pdf_path =self.pdf_path.replace('/', '\\')
            self.newfolderpath = self.newfolderpath.replace('/', '\\')

 
    # Move the PDF file to the destination folder
        try:
            shutil.move(self.pdf_path, self.newfolderpath)
        except:
            pass
    def renamepdfDoc(self):
        fakelos = pattern_f.search(self.text)[0].replace(' ', '')
                # split fakelos to [fak1, fak2, fak3] to catch mistakes
        try:
             
            fak1, upofakelos,prwtokollo,sxedio,dt,sximatismos,grafeio=fakelos.split('/')
            # stoixeia=fakelos.split('/')  
             
            # fak1=stoixeia[0]
            # upofakelos=stoixeia[1]
            # prwtokollo=stoixeia[2]
        except:
                    
            # fak1, upofakelos, prwtokollo = fakelos.split('/')
            stoixeia=fakelos.split('/')  
             
            fak1=stoixeia[0]
            upofakelos=stoixeia[1]
            prwtokollo=stoixeia[2]
            sxedio = pattern_s.search(self.text)[0].replace(' ', '').replace('/', '7')
            dt = pattern_date.search(self.text)[0].replace('/', '7')

        for mistake, fix in mistakes.items():
            fak1 = fak1.replace(mistake, fix)
            upofakelos = upofakelos.replace(mistake, fix)
            prwtokollo = prwtokollo.replace(mistake, fix)
            sxedio = sxedio.replace(mistake, fix)
            dt = dt.replace(mistake, fix)

        new_name = f"{fak1}/{upofakelos}/{prwtokollo}a{sxedio}/{dt}.pdf".replace('/', '_').replace('a', '_')
        oldpath=os.path.join(self.newfolderpath, self.pdf_file)
        newpath=os.path.join(self.newfolderpath, new_name)
        try:
            os.rename(oldpath,newpath )
        except:
            print("yo")
            # Print the recognized text
                # print(f'Page {i + 1}:\n{text}\n')
                # break
        # Clean up temporary image files
            # for i in range(len(images)):
            #     image_path = f'tmp_page_{i}.png'
            #     os.remove(image_path)
            
    def renameDocument(self):
        fakelos = pattern_f.search(self.text)[0].replace(' ', '')
            # split fakelos to [fak1, fak2, fak3] to catch mistakes
        try:
                
            fak1, upofakelos,prwtokollo,sxedio,dt,sximatismos,grafeio,tmima=fakelos.split('/')
        except:
                
            fak1, upofakelos, prwtokollo = fakelos.split('/')
            sxedio = pattern_s.search(self.text)[0].replace(' ', '').replace('/', '7')
            dt = pattern_date.search(self.text)[0].replace('/', '7')

        for mistake, fix in mistakes.items():
            fak1 = fak1.replace(mistake, fix)
            upofakelos = upofakelos.replace(mistake, fix)
            prwtokollo = prwtokollo.replace(mistake, fix)
            sxedio = sxedio.replace(mistake, fix)
            dt = dt.replace(mistake, fix)

        new_name = f"{fak1}/{upofakelos}/{prwtokollo}a{sxedio}/{dt}.pdf".replace('/', '_').replace('a', '_')
        
        
    def extractThemaFromDocument(self)-> str:
        lines = self.text.split('\n')
        index_of_thema = [i for i, line in enumerate(lines) if 'ΘΕΜΑ:' in line]
        if index_of_thema:
            line_following_thema = lines[index_of_thema[0] ]
            substring_to_remove = "ΘΕΜΑ: "
            line_following_thema = line_following_thema .replace(substring_to_remove, "")
            return line_following_thema
        else:
            return "Not found."
    
    def cratefolderWithnameThema(self):
 
        self.newfolderpath=f'{self.currentpath}/{ current_year}_{current_month  }_{current_day  } {self.thema}'
        if not os.path.exists(self.newfolderpath):
            os.makedirs(self.newfolderpath)
 
        else:
  
        # If it exists, find the next available name
            count = 2
            new_folder_name = f"{ current_year}_{current_month  }_{current_day  } {self.thema} ({count})"
            self.newfolderpath = os.path.join(self.currentpath, new_folder_name)

            while os.path.exists(self.newfolderpath):
                count += 1
                new_folder_name = f"{ current_year}_{current_month  }_{current_day  } {self.thema} ({count})"
                self.newfolderpath = os.path.join(self.currentpath, new_folder_name)
            os.makedirs(self.newfolderpath)
        
    def select_folder(self):
        try:
            savedselectedFolder=pathmod.select_folder()

        except:
            pass


    def process_pdfs_in_directory(self):
        pdf_files = [f for f in os.listdir(self.currentpath) if f.endswith('.pdf')]

        for self.pdf_file in pdf_files:
            self.pdf_path = os.path.join(self.currentpath, self.pdf_file)
            extracted_text = self.extract_and_ocr_half_page()
            #print(extracted_text)
            #if extracted_text is not None:
                #print(f"Text from the first half of {pdf_file}:\n")
            # print(extracted_text)
                #print("\n" + "="*50 + "\n")
 

    
    
 