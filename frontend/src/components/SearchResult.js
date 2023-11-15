import React from 'react';
import './SearchResult.css';

function SearchResult({title, subtitle, url, date, authors, pageCount, publication, volume, issue, publisher, languages, wordCount}) {
  return (
    <div className='SearchResult'>
    <h3>{title}{subtitle.length > 0 ? " - " +  subtitle : ""}</h3>
    <h4>Date: {date}</h4>
    <h4>Author(s): {Array.isArray(authors)  ? authors.join(", ") : "N/A"}</h4>
    <h5>Page count: {pageCount}</h5>
    <h5>Publication: {publication} - Volume {volume}, Issue {issue}</h5>
    <h5>Publisher: {publisher}</h5>
    <h5>Word count: {wordCount}</h5>
    <h5>Language(s): {languages.map(elem => elem.toUpperCase()).join(", ")}</h5>
    <h4>Link: <a href={url}>{url}</a></h4>
    </div>
  )
}

export default SearchResult;