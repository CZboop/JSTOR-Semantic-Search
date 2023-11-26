# JSTOR Semantic Search 🕵️‍♀️
Full stack vector search built for JSTOR open source articles - search by meaning, not keywords!

Backend made with a Pinecone vector database, HuggingFace/transformers for embeddings and a FastAPI API with two endpoints for making queries with or without metadata filters.
Frontend made with React.js

## Project Summary 📝
This project is intended to be used with local datasets built from [JSTOR's official data partner Constellate](https://constellate.org/), in JSONL format from the full data download option.

Currently, the titles and subtitles of articles are combined and embedded, and a semantic similarity is measured from the query to these embedded titles and subtitles. More detailed information about the articles is returned as part of the metadata. 

Through the API and the frontend web app, the desired Top K number of results can be passed through, and filters such as date and page count can also be passed, in the form of a filter dictionary using the [Pinecone metadata query language](https://docs.pinecone.io/docs/metadata-filtering#metadata-query-language).

Through the API, the dictionary of metadata filters should directly reflect the dictionary format that can be passed to Pinecone, although the web app will handle adding the keys and the user can input just the values in a form.

## Setup and How to Use 🔧
### Backend Setup 🐍
#### Python and Dependency Installation 📦
To get set up with Python and the dependencies to run this project:

* If Python is not installed, install it from [this link](https://www.python.org/downloads/).  
* Clone this repository, then navigate to the directory it is in.  
* Set up a virtual environment using:  
```$ python -m venv <evironment_name>```  
* Activate the virtual environment. For Windows cmd, this is done using:  
```$ <evironment_name>\Scripts\activate.bat```  
[This link](https://docs.python.org/3/library/venv.html) shows how to do this for other operating systems and shell types.
* Install dependencies using:  
```$ pip install -r requirements.txt ```  
* After navigating to the directory with the desired file, one of the Python files can be run using:  
```$ python <filename>.py```  

#### Pinecone Setup 🌲
* Create a Pinecone account if needed on [their website](https://www.pinecone.io/). Each user can create one free index at a time, and you can delete and remake this index as many times as you want.
* Get your API key and environment from the 'API Keys' page
* Save these in a file called .env in the backend folder, in the following format:
  ```
  PINECONE_API_KEY='<YOUR API KEY>'
  PINECONE_ENV='<YOUR ENVIRONMENT>'
  ```

#### Adding Data 💾
To add data to your Pinecone index:
* First download a dataset or multiple datasets from [Constellate](https://constellate.org/). There are limits to how many documents can be in each dataset but you can pull multiple.
* Extract your data and move it into a directory within this cloned project, ideally a /data folder in the /backend directory.
* Create an instance of the DBWriter class from the db_writerr.py file, updating the list of paths_to_data in the constructor to match where you put your data files, and updating the index_name to the name of your Pinecone index ('jstor-semantic-search' by default).
* Call the .run() method of the new DBWriter instance.

This should embed and upsert all the items in the dataset into your Pinecone index. Note, this adds to the current index, so if you want only the new data to be inside the index, you should delete the index first which can be done with the ._delete_index() method of the DBClient class within this repository.

#### Running the API 🏃
From the /backend folder, the API can be run by either:
- ```$ uvicorn main:app``` Which won't update the API with any development changes, but can be shut down easily with a Ctrl + c in the terminal
- ```$ uvicorn main:app --reload``` Which will update the API with any development changes, but won't shut down with Ctrl + c

#### API Endpoints 🌐
The API has two endpoints, one for a simple query only search, and one for a search with query plus metadata filters. However, the way that the filters are processed means that the filtered endpoint will work with an empty dict, and is therefore the only endpoint called from the web app.

`GET` **`/api/v1/query/{query_string}/{top_n}`**

Takes two path parameters:
    - query_string (data type: string) - The main search query that should be semantically similar to the results the user wants
    - top_n (data type: integer) - The number of matches to return

`POST` **`/api/v1/filter-query/{query_string}/{top_n}`**

Takes the same two path parameters:
    - query_string (data type: string) - The main search query that should be semantically similar to the results the user wants
    - top_n (data type: integer) - The number of matches to return
    
Plus a filter dict in the request body, for example:
```json
{
    "document_type": {"$eq" : "document"},
    "word_count": {"$gte": 2000}
}
```

Both endpoints return the same type of response, with main results as an array within the 'matches' key, for example:

```json
{
  "matches": [
    {
      "id": "123-abc-321",
      "score": 18.792,
      "values": [],
      "metadata": {
        "categories": [
          "Language & Literature",
          "Humanities"
        ],
        "creator": [
          "A. Creator"
        ],
        "date_published": "2020/04/01",
        "document_sub_type": "",
        "document_type": "document",
        "issue_number": "1",
        "language": [
          "eng"
        ],
        "page_count": 10.0,
        "parent_publication": "A publication",
        "publisher": "A publisher",
        "sub_title": "",
        "title": "An example",
        "url": "http://www.jstor.org/stable/1234",
        "volume_number": "2123",
        "word_count": 123.0
      }
    }
  ],
  "namespace": ""
}
```

### Frontend Setup ⚛️
Once the backend is set up and the API is running, you should be able to use the web app to interact with the API and search more easily.
To do this:
- Navigate to the /frontend folder in the cloned respository (in a separate terminal from the one running the API)
- Run ```$ npm install``` to install dependencies
- Run ```$ npm start``` to start the web app locally
- The site should open automatically, and you can also navigate to http://localhost:3000/ to use it
