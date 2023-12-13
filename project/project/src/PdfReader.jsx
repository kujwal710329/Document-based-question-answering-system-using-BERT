import React, { useEffect, useState } from "react";
import { pdfjs, Document, Page } from "react-pdf";
import unorm from "unorm";
import "./App.css";
import axios from "axios";

// Ensure workerSrc property is set to the correct path to pdf.worker.js
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

const PdfReader = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [custom, setCustom] = useState("");
  const [numPages, setNumPages] = useState(null);

  useEffect(() => {
    try {
      const response = axios.post(
        "http://localhost:8000/get_data",
        { data: custom ? custom : text },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(text);
      console.log(response);
      console.log("api response", response.data);
      // setText(custom ? custom : text);
    } catch (error) {
      console.error("error submitting data", error);
    }
  }, [text]);
  const handleSubmit = async (e) => {
    e.preventDefault();
    // try {
    //   const response = await axios.post(
    //     "http://localhost:8000/get_data",
    //     { data: custom ? custom : text },
    //     {
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //     }
    //   );
    //   console.log(text);
    //   console.log(response);
    //   console.log("api response", response.data);
    //   setText(custom ? custom : text);
    // } catch (error) {
    //   console.error("error submitting data", error);
    // }

    setText(custom);
  };
  const onFileChange = async (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);

      // Convert PDF to text
      const text = await convertPdfToText(selectedFile);
      setText(text);
    }
  };

  const convertPdfToText = async (pdfFile) => {
    const reader = new FileReader();

    return new Promise((resolve) => {
      reader.onload = async (event) => {
        const typedArray = new Uint8Array(event.target.result);
        const loadingTask = pdfjs.getDocument({ data: typedArray });

        loadingTask.promise.then(async (pdf) => {
          let pdfText = "";

          for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map((s) => unorm.nfc(s.str)).join(" ");
            pdfText += pageText;
            // pdfText += textContent.items.map((s) => s.str).join(" ");
          }
          // pdfText = pdfText.items.map((s) => s.str.normalize("NFC")).join(" ");
          setNumPages(pdf.numPages);
          resolve(pdfText);
        });
      };

      reader.readAsArrayBuffer(pdfFile);
    });
  };

  return (
    <div className="container">
      <h1>PDF Reader</h1>

      <input type="file" accept=".pdf" onChange={onFileChange} />
      <form onSubmit={handleSubmit}>
        <label>
          Enter custom paragraph:
          <input type="text" onChange={(event) => setCustom(event.target.value)} />
        </label>
        <button type="submit">Update</button>
      </form>
      {/* {file && (
        <div>
          <h2>Number of Pages: {numPages}</h2>
          <div>
            <Document file={file}>
              {Array.from(new Array(numPages), (el, index) => (
                <Page key={`page_${index + 1}`} pageNumber={index + 1} />
              ))}
            </Document>
          </div>
          <h2>Text Content:</h2>
          <p>{text}</p>
        </div>
      )} */}
      <h2>Text content:</h2>
      <p>{text}</p>
    </div>
  );
};

export default PdfReader;
