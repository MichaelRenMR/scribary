from PyPDF2 import PdfFileReader
import argparse
import io
import json
import os

from google.cloud import language_v1
import numpy
import six

def classify(result, text, verbose=False):
    language_client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={'document': document})
    categories = response.categories

    for category in categories:
        print(category.name, category.confidence)
        # if category.confidence >= 0.7:
        #     print("LARGE CONFIDENCE")
        # splits category name into subcategories
        category_arr = category.name.split("/")

        # Takes the max confidence of that category type
        if category_arr[1] not in result.keys():
            result[category_arr[1]] = category.confidence
        else:
            result[category_arr[1]] = max(result[category_arr[1]], category.confidence)
        print("*******************")

    if verbose:
        for category in categories:
            print(u"=" * 20)
            print(u"{:<16}: {}".format("category", category.name))
            print(u"{:<16}: {}".format("confidence", category.confidence))
    return result


def generate_tags(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        result = {}
        number_of_pages = pdf.getNumPages()
        for a in range(number_of_pages):
            page = pdf.getPage(a)
            text = page.extractText()
            text = text.split(". ")
            sentences = ""
            i = 0

            while i < len(text):
                sentences = ""
                while len(sentences) < 300 and i < len(text):
                    sentences += text[i]
                    i += 1
                if len(sentences) >= 175:
                    result = classify(result, sentences)
        print(result)
        print(len(result))
        return result


def main():
    pdf_path = "healthcare.pdf"
    x = generate_tags(pdf_path)

if __name__ == "__main__":
    main()


# tags = generate_tags('healthcare.pdf')
