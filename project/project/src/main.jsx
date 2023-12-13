import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import PdfReader from "./PdfReader.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <div className="main">
      <PdfReader />
      <App />
    </div>
  </React.StrictMode>
);
