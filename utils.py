import io
import copy
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

class DEFINED_DIMENSION:
    WIDTH=3480
    HEIGHT=3480


def get_per_page_split(runnning_page_height):
    no_of_split=runnning_page_height//DEFINED_DIMENSION.HEIGHT
    reminder = runnning_page_height % DEFINED_DIMENSION.HEIGHT
    if reminder !=0 :
        no_of_split=no_of_split+1
    return no_of_split


def split_into_mul_pages(page, runnning_page_height, writer):
    page_break = 0
    if runnning_page_height <= DEFINED_DIMENSION.HEIGHT:
        no_of_split=1
    else:
        no_of_split = get_per_page_split(runnning_page_height)
    page_upperleft = page.mediaBox.upperLeft
    page_list=list()
    for i in range(no_of_split):
        
        part=copy.deepcopy(page)
        print(type(part))
        part.mediaBox.upperLeft = page_upperleft
        part.mediaBox.LowerLeft = (page_upperleft[0], page_upperleft[1]-DEFINED_DIMENSION.HEIGHT)
        page_upperleft = (page_upperleft[0], page_upperleft[1]-DEFINED_DIMENSION.HEIGHT)
        page_list.append(part)
    
        writer.addPage(part)
    with open("expected_out.pdf", "wb+") as f:
        writer.write(f)
    return writer
   


def process_file(contents):
    chunk_pdf = PdfFileReader(
            stream=io.BytesIO(      # Create steam object
                initial_bytes=contents
            )
        )

    num_pages = chunk_pdf.getNumPages()
    print(num_pages)
    writer = PdfFileWriter()
    for page_no in range(num_pages):
        running_page = chunk_pdf.getPage(page_no)
        running_page_lowerright = running_page.mediaBox.lowerRight
        running_page_upperleft = running_page.mediaBox.upperLeft
        running_page_width = running_page_lowerright[0]
        runnning_page_height = running_page_upperleft[1]
        dim_multiplier = 1
        if running_page_width > DEFINED_DIMENSION.WIDTH:
            dim_multiplier = 3480/dim_multiplier

        running_page_width *= dim_multiplier
        runnning_page_height *= dim_multiplier
        print(runnning_page_height)
        running_page.mediaBox.upperRight = (running_page_width, int(runnning_page_height))
        writer = split_into_mul_pages(running_page, runnning_page_height, writer)
        
    

    # with open("expected_out.pdf", "wb+") as f:
    #     writer.write(f)
        

        


if __name__ == "__main__":
    with open('Expected_Output.pdf', 'rb') as f:
        contents = f.read()
        process_file(contents)




