import React from 'react';

function SearchResult({title, url}) {
  return (
    <div className='SearchResult'>
    <h3>{title}</h3>
    <h4>{url}</h4>
    </div>
  )
}

export default SearchResult;