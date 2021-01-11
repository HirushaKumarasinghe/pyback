# import text_retriever
from pyresparser import ResumeParser

def gather_data(type,direcotry):

    if (type == 'pdf'):
        data = ResumeParser("./test_data/cv.pdf").get_extracted_data()

    elif (type == 'img'):
        data = ResumeParser("./test_data/cv.pdf").get_extracted_data()

    else:
        return 0

    # text_data = text_retriever.retrieve_text()
    # print(data)
    return data

gather_data()

