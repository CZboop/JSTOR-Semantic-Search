import './App.css';
import { useState, useEffect } from 'react';
import SearchResult from './components/SearchResult.js';
import API from './API.js';

function App() {
  const [queryString, setQueryString] = useState("");
  const [queryResponse, setQueryResponse] = useState([]);
  const [dateFrom, setDateFrom] = useState("2017");
  const [dateTo, setDateTo] = useState("2023");
  const [wordsFrom, setWordsFrom] = useState(1);
  const [wordsTo, setWordsTo] = useState(50000);
  const [pagesFrom, setPagesFrom] = useState(1);
  const [pagesTo, setPagesTo] = useState(500);
  const [docType, setDocType] = useState("Articles");
  const [DBFilters, setDBFilters] = useState({});
  const [topK, setTopK] = useState(5);

  // turning into filters that can be passed to pinecone from the form data
  const makeDBFiltersFromForm = () => {
    const filters = {
      "page_count": {"$gte" : parseInt(pagesFrom, 10), "$lte" : parseInt(pagesTo, 10)},
      "word_count": {"$gte" : parseInt(wordsFrom, 10), "$lte" : parseInt(wordsTo, 10)},
      "date_published": {"$gte" : dateFrom, "$lte" : dateTo}
    };
    setDBFilters(filters);
  }

  const makeQuery = async (e) => {
    e.preventDefault()
    console.log(DBFilters);
    const result = await API.post(`/api/v1/filter-query/${queryString}/${topK}`, DBFilters);
    const resultMatches = result.data["matches"];
    setQueryResponse(resultMatches);
    console.log(resultMatches);
  }

  useEffect(() => {},
    [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>JSTOR Semantic Search</h1>
        <h3>Search by meaning, not keywords!</h3>
      </header>
      <form className='query-form' onSubmit={makeQuery}>
        <div className='queryStringContainer'>
          <label>Search query: </label>
          <input id='searchBar' type='text' value={queryString} onChange={(e) => {
            setQueryString(e.target.value);
            makeDBFiltersFromForm();
            }} required/>
          
          </div>
          <div className='topKContainer'>
          <label>Number of results: </label>
          <input id='topK' type='number' value={topK} onChange={(e) => {
            setTopK(e.target.value);
            makeDBFiltersFromForm();
            }} 
            min="1" max="50"
            required/>
          
          </div>
          <hr></hr>
          <div className='filtersContainer'>
          <h4 id='filtersHeading'>
            Filters (optional)
          </h4>
          <div className='filterContainer'>
          <h5>Word count:</h5>
          <div className='filterInputs'>
            <p>From:</p>
            <input type="number" className='wordCountInput' id="wordCountFrom" name="wordCountFrom" min="1" 
            value={wordsFrom} onChange={(e) => {
              setWordsFrom(e.target.value);
              makeDBFiltersFromForm();
            }}
            />
            <p>To:</p>
            <input type="number" className='wordCountInput' id="wordCountTo" name="wordCountTo" min="1"
            value={wordsTo} onChange={(e) => {
              setWordsTo(e.target.value);
              makeDBFiltersFromForm();
            }}
            />
            </div>
          </div>
          <div className='filterContainer'>
          <h5>Page count:</h5>
          <div className='filterInputs'>
            <p>From:</p>
            <input type="number" className='pageCountInput' id="pageCountFrom" name="pageCountFrom" min="1"
            value={pagesFrom} onChange={(e) => {
              setPagesFrom(e.target.value);
              makeDBFiltersFromForm();
            }}
            />
            <p>To:</p>
            <input type="number" className='pageCountInput' id="pageCountTo" name="pageCountTo" min="1"
            value={pagesTo} onChange={(e) => {
              setPagesTo(e.target.value);
              makeDBFiltersFromForm();
            }}
            />
            </div>
          </div>
          {/* TODO: further be able to filter once you have results, based on their values which will be more limited? */}
          <div className='filterContainer'>
          <h5>Date:</h5>
          <p>(yyyy or yyyy/mm or yyyy/mm/dd)</p>
          {/* (yyyy or yyyy/mm or yyyy/mm/dd) dates to allow user friendly way to go far back */}
          <div className='filterInputs'>
            <p>From:</p>
            <input type="text" id="dateFrom" name="dateFrom"
            value={dateFrom} onChange={(e) => {
              setDateFrom(e.target.value);
              makeDBFiltersFromForm();
            }}
            />
            <p>To:</p>
            <input type="text" id="dateTo" name="dateTo"
            value={dateTo} onChange={(e) => {
              setDateTo(e.target.value);
              makeDBFiltersFromForm();
            }}
            />
            </div>
          </div>
          <div className='filterContainer'>
          <h5>Document Type:</h5>
          {/* Types of content (map value to how show in metadata): 
          Articles
          Research Reports
          Reviews
          Miscellaneous
          Books */}
          <select name="docTypes" id="docTypes" 
          value={docType} onChange={(e) => {
            setDocType(e.target.value);
            makeDBFiltersFromForm();
          }}
          >
            <option value="article">Articles</option>
            <option value="report">Research Reports</option>
            <option value="review">Reviews</option>
            <option value="book">Books</option>
            <option value="miscellaneous">Miscellaneous</option>
          </select>
          </div>
          
            {/* NOTE: believe the endpoint with metadata could be fine with no metadata if removes all keys from dict? */}
          
          </div>
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
