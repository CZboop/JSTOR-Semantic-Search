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
  const makeDBFiltersFromForm = (form) => {
    const filters = {
      "page_count": {"$gte" : parseInt(form.pageCountFrom.value, 10), "$lte" : parseInt(form.pageCountTo.value, 10)},
      "word_count": {"$gte" : parseInt(form.wordCountFrom.value, 10), "$lte" : parseInt(form.wordCountTo.value, 10)},
      "date_published": {"$gte" : form.dateFrom.value.replaceAll("-", "/"), "$lte" : form.dateTo.value.replaceAll("-", "/")},
      "document_type": {"$eq": form.docTypes.value}
    };
    setDBFilters(filters);
  }

  const makeQuery = async (e) => {
    e.preventDefault()
    makeDBFiltersFromForm(e.target);
    // console.log(DBFilters);
    try{ 
      const result = await API.post(`/api/v1/filter-query/${queryString}/${topK}`, DBFilters);
      const resultMatches = result.data["matches"];
      if (resultMatches.length > 0) {
        setQueryResponse(resultMatches);
        console.log(resultMatches);
      }
      else{
        console.log("NO RESULTS!");
        // TODO: modal to say no results returned try again, try without filters first etc.
      }

    } catch (e) {
      console.log("SOMETHING WENT WRONG, SEE ERROR MESSAGE BELOW");
      console.log(e.toJSON());
      // TODO: modal with diff messages depending on error?
    }
    
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
          <input id='searchBar' name='searchBar' type='text' value={queryString} onChange={(e) => {
            setQueryString(e.target.value);
            }} required/>
          
          </div>
          <div className='topKContainer'>
          <label>Number of results: </label>
          <input id='topK' name='topK' type='number' value={topK} onChange={(e) => {
            setTopK(e.target.value);
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
            }}
            />
            <p>To:</p>
            <input type="number" className='wordCountInput' id="wordCountTo" name="wordCountTo" min="1"
            value={wordsTo} onChange={(e) => {
              setWordsTo(e.target.value);
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
            }}
            />
            <p>To:</p>
            <input type="number" className='pageCountInput' id="pageCountTo" name="pageCountTo" min="1"
            value={pagesTo} onChange={(e) => {
              setPagesTo(e.target.value);
            }}
            />
            </div>
          </div>
          {/* TODO: further be able to filter once you have results, based on their values which will be more limited? */}
          <div className='filterContainer'>
          <h5>Date:</h5>
          <div className='filterInputs'>
            <p>From:</p>
            <input type="date" id="dateFrom" name="dateFrom"
            value={dateFrom} onChange={(e) => {
              setDateFrom(e.target.value);
            }}
            />
            <p>To:</p>
            <input type="date" id="dateTo" name="dateTo"
            value={dateTo} onChange={(e) => {
              setDateTo(e.target.value);
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
            // makeDBFiltersFromForm();
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
