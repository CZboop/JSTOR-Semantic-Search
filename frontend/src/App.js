import './App.css';
import { useState, useEffect } from 'react';
import SearchResult from './components/SearchResult.js';

function App() {
  const [queryString, setQueryString] = useState("");
  const [queryResponse, setQueryResponse] = useState([]);

  const makeQuery = async (e) => {
    e.preventDefault()
    const response = await fetch("http://localhost:8000/api/v1/query/" + queryString,
      {
        method: 'get'
      }
    )
    const result = await response.json()
    const resultMatches = result["matches"]
    setQueryResponse(resultMatches);
    console.log(resultMatches);
  }

  useEffect(() => {},
    [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>JSTOR Semantic Search</h1>
      </header>
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
        <div className='search-results'>
          {
            queryResponse.length > 0 ?
            <>
            <hr className='resultsRuler'></hr>
            <h2>Search Results</h2>
            {queryResponse.map(response => 
              <SearchResult 
                title={response.metadata.title} 
                subtitle={response.metadata.sub_title} 
                date={response.metadata.date_published}
                authors={response.metadata.creator} // array
                pageCount={response.metadata.page_count} // float convert to int?
                publication={response.metadata.parent_publication}
                volume={response.metadata.volume_number}
                issue={response.metadata.issue_number}
                publisher={response.metadata.publisher}
                languages={response.metadata.language} // array
                wordCount={response.metadata.word_count} // float to convert?
                url={response.metadata.url} 
                key={response.metadata.url} 
              />)
            }
            </>
            :
            <></>
          }

        </div>
    </div>
  );
}

export default App;
