import React, { useState } from 'react';
import resume from '../Assets/resume.pdf';
import { SizeMe } from 'react-sizeme';
import { Document, Page, pdfjs } from 'react-pdf';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const PDFViewer = props => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  let pdfURL = props.pdfURL;
  console.log(pdfURL);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  /* Use SizeMe to dynamically resize the document */
  return (
    <div style={{width: '80%'}}>
      <SizeMe
        monitorHeight
        refreshRate={128}
        refreshMode={"debounce"}
        render={({ size }) => (
          <div className="pdf-resume">
            <Document
                file={pdfURL}
                onLoadSuccess={onDocumentLoadSuccess}
            >
              <div>
                <Page
                  width={size.width}
                  pageNumber={pageNumber}
                  renderMode="svg"
                />
              </div>
            </Document>
          </div>
        )}
      />
    </div>
  );
}

export default PDFViewer;
