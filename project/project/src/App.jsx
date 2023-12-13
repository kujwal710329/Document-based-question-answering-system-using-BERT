import React, { useState, useEffect } from "react";
import axios from "axios";
// import Loader from "react-loader-spinner";
import "./App.css";
function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async (event) => {
    setLoading(true);
    event.preventDefault();

    try {
      const response = await axios.post(
        "http://localhost:8000/ask_question",
        { data: question },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(question);
      console.log(response);
      console.log("api response", response.data);
      setAnswer(response.data.corrected_answer);
      setLoading(false);
    } catch (error) {
      console.error("error submitting data", error);
    }

    // setAnswer(question.normalize("NFC"));
  };
  // useEffect(() => {
  //   handleSubmit();
  // }, []);

  return (
    <div className="container">
      <h1>Question Answer System</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter your question:
          <input type="text" value={question} onChange={handleQuestionChange} />
        </label>

        <button type="submit">Ask Question</button>
      </form>
      {/* {answer && (
        <div>
          <h2>Answer:</h2>
          <p>{answer}</p>
        </div>
      )} */}
      {loading ? (
        // Display the loader while waiting for the API response
        // <Loader type="Puff" color="#00BFFF" height={100} width={100} />
        <p>Hold On ... BERT IS DOING THEIR WORK😀</p>
      ) : answer ? (
        // Display the answer if available
        <div>
          <h2>Answer:</h2>
          <p>{answer}</p>
        </div>
      ) : null}
    </div>
  );
}

export default App;
