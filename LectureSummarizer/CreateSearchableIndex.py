#! /usr/bin/env python3
import pypdf
import os
# helper function to create a list of all absolute paths for all files in the lecture_files subdirectory
def find_lecture_PDFs():
    path = './lecture_files'
    list_of_lectures = []
    for dir in os.listdir(path):  
        test_path = path + '/' + dir
        if os.path.isfile(test_path):
            list_of_lectures.append(test_path)
    return list_of_lectures

# main function which converts the PDFs into files based on the list of paths that is provided. 
def convert_lectures_pdf(list_of_lectures):
    if type(list_of_lectures) == list:
        for file in list_of_lectures:
            # strip out the file name from the absolute path
            filename = file[file.rfind('/')+1:file.rfind('.')]
            # try opening the pdf, raise an exception to the user for any error
            try:
                pdf_file = pypdf.PdfReader(file)
            except:
                print('Sorry there was an error in processing the PDF. Please contact send the pdf to rrafiq0@chicagobooth.edu with the error log')
            else:
                # cycle through and convert the text for every page. At the top of every page include the filename, and the pagenumber
                for page in pdf_file.pages:
                    #append to the end of the file
                    with open('lecture_index.txt', 'a') as my_file:
                        my_file.write('\nFILENAME: ' + filename + '\nPAGENUMBER: ' + str(page.page_number) + '\n')
                        text = page.extract_text()
                        my_file.write(text)
                        #print(text)
    else:
        print('Sorry but you must provide a list of valid file paths')

# main driver for calling code
def main():
    list_of_lectures = find_lecture_PDFs()
    convert_lectures_pdf(list_of_lectures)

if __name__ == '__main__':
    main()


