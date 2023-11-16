import './App.css';
import { useState, useEffect, createContext } from 'react';
import SearchResult from './components/SearchResult.js';
import API from './API.js';
import Modal from './components/Modal.js';

export const ModalContext = createContext();

function App() {
  const [queryString, setQueryString] = useState("");
  const [queryResponse, setQueryResponse] = useState([]);

  const [dateFrom, setDateFrom] = useState("2017-01-01");
  const [dateTo, setDateTo] = useState("2023-12-12");
  const [wordsFrom, setWordsFrom] = useState(1);
  const [wordsTo, setWordsTo] = useState(50000);
  const [pagesFrom, setPagesFrom] = useState(1);
  const [pagesTo, setPagesTo] = useState(500);
  const [docType, setDocType] = useState("Articles");
  const [topK, setTopK] = useState(5);

  const [modalOpen, setModalOpen] = useState(false);
  const [modalTitle, setModalTitle] = useState("Error");
  const [modalMessage, setModalMessage] = useState("Something went wrong");

  const makeQuery = async (e) => {
    e.preventDefault()
    // turning the form data into filters that can be passed to pinecone, doing this way to prevent state being out of date
    let DBFilters = {
      "page_count": {"$gte" : parseInt(e.target.pageCountFrom.value, 10), "$lte" : parseInt(e.target.pageCountTo.value, 10)},
      "word_count": {"$gte" : parseInt(e.target.wordCountFrom.value, 10), "$lte" : parseInt(e.target.wordCountTo.value, 10)},
      "date_published": {"$gte" : e.target.dateFrom.value.replaceAll("-", "/"), "$lte" : e.target.dateTo.value.replaceAll("-", "/")},
      "document_type": {"$eq": e.target.docTypes.value}
    };
    console.log(DBFilters);
    try{ 
      const result = await API.post(`/api/v1/filter-query/${queryString}/${topK}`, DBFilters);
      const resultMatches = result.data["matches"];
      if (resultMatches.length > 0) {
        setQueryResponse(resultMatches);
        console.log(resultMatches);
      }
      else{
        setModalMessage("No results were found for that query. Try again, maybe clearing any filters first");
        setModalTitle("No Results");
        setModalOpen(true);
      }

    } catch (e) {
      setModalMessage("Something went wrong: " + JSON.stringify(e.toJSON().message));
      setModalTitle("Error While Making Request");
      setModalOpen(true);
    }
    
  }

  useEffect(() => {},
    [])

  return (
    <div className="App">
      <header className="App-header contentContainer">
        <h1>JSTOR Semantic Search 🕵️‍♀️</h1>
        <h3 id='subTitle'>Search by meaning, not keywords!</h3>
      </header>
      <ModalContext.Provider value={{setModalOpen, setModalTitle, setModalMessage}}>
          <Modal open={modalOpen} title={modalTitle} message={modalMessage} />
      </ModalContext.Provider>
      <form className='query-form contentContainer' onSubmit={makeQuery}>
        <div className='queryStringContainer'>
          <label>Search query: </label>
          <input id='searchBar' name='searchBar' type='text' value={queryString} onChange={(e) => {
            setQueryString(e.target.value);
            }} required/>
          
          </div>
          <div className='formHeading'>
          <label>Number of results: </label>
          <input id='topK' name='topK' type='number' value={topK} onChange={(e) => {
            setTopK(e.target.value);
            }} 
            min="1" max="50"
            required/>
          
          </div>
          <div className='filtersContainer'>
          <h4 id='filtersHeading' className='formHeading'>
            Filters
          </h4>
          <div className='filterContainer'>
          <h5 className='formHeading'>Word count:</h5>
          <div className='filterInputs'>
            <p className='formHeading'>From:</p>
            <input type="number" className='wordCountInput' id="wordCountFrom" name="wordCountFrom" min="1" 
            value={wordsFrom} onChange={(e) => {
              setWordsFrom(e.target.value);
            }} required
            />
            <p className='formHeading'>To:</p>
            <input type="number" className='wordCountInput' id="wordCountTo" name="wordCountTo" min="1"
            value={wordsTo} onChange={(e) => {
              setWordsTo(e.target.value);
            }} required
            />
            </div>
          </div>
          <div className='filterContainer'>
          <h5 className='formHeading'>Page count:</h5>
          <div className='filterInputs'>
            <p className='formHeading'>From:</p>
            <input type="number" className='pageCountInput' id="pageCountFrom" name="pageCountFrom" min="1"
            value={pagesFrom} onChange={(e) => {
              setPagesFrom(e.target.value);
            }} required
            />
            <p className='formHeading'>To:</p>
            <input type="number" className='pageCountInput' id="pageCountTo" name="pageCountTo" min="1"
            value={pagesTo} onChange={(e) => {
              setPagesTo(e.target.value);
            }}
            />
            </div>
          </div>
          <div className='filterContainer'>
          <h5 className='formHeading'>Date:</h5>
          <div className='filterInputs'>
            <p className='formHeading'>From:</p>
            <input type="date" id="dateFrom" name="dateFrom"
            value={dateFrom} onChange={(e) => {
              setDateFrom(e.target.value);
            }} required
            />
            <p className='formHeading'>To:</p>
            <input type="date" id="dateTo" name="dateTo"
            value={dateTo} onChange={(e) => {
              setDateTo(e.target.value);
            }} required
            />
            </div>
          </div>
          <div className='filterContainer'>
          <h5 className='formHeading'>Document Type:</h5>
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
                key={response.id} 
              />)
            }
            </>
            :
            <></>
          }

        </div>
        <a href='#' className='scrollTop'>^^Back to top^^</a>
    </div>
  );
}

export default App;
