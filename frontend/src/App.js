import './App.css';
import { useState, useEffect } from 'react';

function App() {
  const [queryString, setQueryString] = useState("");
  const [queryResponse, setQueryResponse] = useState("");

  const makeQuery = async (e) => {
    e.preventDefault()
    const response = await fetch("http://localhost:8000/api/v1/query/" + queryString)
    const result = await response.json()
    setQueryResponse(result.data);
    console.log(queryResponse);
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>JSTOR Semantic Search</h1>
        <form className='query-form' onSubmit={makeQuery}>
          <label> 
            Query string:
            <input type='text' value={queryString} onChange={(e) => setQueryString(e.target.value)} required/>
          </label>
          <label>
            Filters
            {/* TODO: filters once string only query can be made and show results*/}
          </label>
          <button >Submit</button>
        </form>
      </header>
    </div>
  );
}

export default App;
