import unittest, pytest
from backend.data_handler import DataHandler
import pandas as pd
from pandas.testing import assert_frame_equal
import json
import pathlib
import transformers.models

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()

class TestDataHandler(unittest.TestCase):

    maxDiff = None

    # == TEST LOAD DATA == #

    def test_load_data_returns_df_with_expected_data(self):
        # given - a data handler instance reading in a single file of data with know values
        data_as_dicts = [
            {"creator": ["Michael Test"], "datePublished": "2013-04-01", "docType": "document", "doi": "20.1.2.3.4", "id": "http://www.test.org/stable/20.1.2.3.4", "identifier": [{"name": "doi", "value": "20.1.2.3.4"}, {"name": "issn", "value": "201234"}, {"name": "oclc", "value": "201234"}, {"name": "lccn", "value": "201234"}, {"name": "local_uuid", "value": "201234-hhhhhhh"}], "isPartOf": "Journal of Testing", "issueNumber": 1, "keyphrase": ["testing", "test"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 1, "pageEnd": 100, "pageStart": 100, "pagination": "pp. 100", "provider": "jstor", "publicationYear": 2013, "publisher": "Test Press", "sourceCategory": ["Test"], "tdmCategory": ["Technology"], "title": "Testing - A JSONL object", "url": "http://www.test.org/stable/20.1.2.3.4", "volumeNumber": 10, "wordCount": 100, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "review", "subTitle": "An Analysis of Testing Methods", "abstract": "An abstract"},
            {"creator": ["Samira Tester"], "datePublished": "2015-04-02", "docType": "document", "doi": "20.1.2.3.5", "id": "http://www.test.org/stable/20.1.2.3.5", "identifier": [{"name": "doi", "value": "20.1.2.3.5"}, {"name": "issn", "value": "201235"}, {"name": "oclc", "value": "201235"}, {"name": "lccn", "value": "201235"}, {"name": "local_uuid", "value": "201235-iiiii"}], "isPartOf": "Testing Today", "issueNumber": 2, "keyphrase": ["software testing", "data"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 20, "pageEnd": 100, "pageStart": 80, "pagination": "pp. 80-100", "provider": "jstor", "publicationYear": 2015, "publisher": "Testing Example", "sourceCategory": ["Example"], "tdmCategory": ["Technology"], "title": "Software Testing in JSON Format", "url": "http://www.test.org/stable/20.1.2.3.5", "volumeNumber": 15, "wordCount": 2000, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "article", "subTitle": "A Comprehensive Review", "abstract": "Another abstract"},
            {"creator": ["Saif Tested"], "datePublished": "2017-04-02", "docType": "document", "doi": "20.1.2.3.6", "id": "http://www.test.org/stable/20.1.2.3.6", "identifier": [{"name": "doi", "value": "20.1.2.3.6"}, {"name": "issn", "value": "201236"}, {"name": "oclc", "value": "201236"}, {"name": "lccn", "value": "201236"}, {"name": "local_uuid", "value": "201236-jjjjj"}], "isPartOf": "Testing Today", "issueNumber": 2, "keyphrase": ["software testing", "examples"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 10, "pageEnd": 90, "pageStart": 80, "pagination": "pp. 80-90", "provider": "jstor", "publicationYear": 2017, "publisher": "Fake Publisher", "sourceCategory": ["Software"], "tdmCategory": ["Technology"], "title": "Testing", "url": "http://www.test.org/stable/20.1.2.3.6", "volumeNumber": 8, "wordCount": 500, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "article", "subTitle": "Key Developments 2017", "abstract": "The third abstract"}
            ]
        with open(f'{CURRENT_DIR}/test_data/test_data1.jsonl', 'w') as file_:
            for item in data_as_dicts:
                file_.write(json.dumps(item) + "\n")

        undertest = DataHandler(paths_to_data = [f'{CURRENT_DIR}/test_data/test_data1.jsonl'])

        # when - we call the load data method
        actual_df = undertest._load_data()
        expected_df = pd.DataFrame.from_dict(data_as_dicts)
        # then - a dataframe version of the data is returned
        assert_frame_equal(actual_df, expected_df)

    def test_load_data_sets_class_attr_with_expected_data(self):
        # given - a data handler instance reading in a single file of data with know values
        data_as_dicts = [
            {"creator": ["Michael Test"], "datePublished": "2013-04-01", "docType": "document", "doi": "20.1.2.3.4", "id": "http://www.test.org/stable/20.1.2.3.4", "identifier": [{"name": "doi", "value": "20.1.2.3.4"}, {"name": "issn", "value": "201234"}, {"name": "oclc", "value": "201234"}, {"name": "lccn", "value": "201234"}, {"name": "local_uuid", "value": "201234-hhhhhhh"}], "isPartOf": "Journal of Testing", "issueNumber": 1, "keyphrase": ["testing", "test"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 1, "pageEnd": 100, "pageStart": 100, "pagination": "pp. 100", "provider": "jstor", "publicationYear": 2013, "publisher": "Test Press", "sourceCategory": ["Test"], "tdmCategory": ["Technology"], "title": "Testing - A JSONL object", "url": "http://www.test.org/stable/20.1.2.3.4", "volumeNumber": 10, "wordCount": 100, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "review", "subTitle": "An Analysis of Testing Methods", "abstract": "An abstract"},
            {"creator": ["Samira Tester"], "datePublished": "2015-04-02", "docType": "document", "doi": "20.1.2.3.5", "id": "http://www.test.org/stable/20.1.2.3.5", "identifier": [{"name": "doi", "value": "20.1.2.3.5"}, {"name": "issn", "value": "201235"}, {"name": "oclc", "value": "201235"}, {"name": "lccn", "value": "201235"}, {"name": "local_uuid", "value": "201235-iiiii"}], "isPartOf": "Testing Today", "issueNumber": 2, "keyphrase": ["software testing", "data"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 20, "pageEnd": 100, "pageStart": 80, "pagination": "pp. 80-100", "provider": "jstor", "publicationYear": 2015, "publisher": "Testing Example", "sourceCategory": ["Example"], "tdmCategory": ["Technology"], "title": "Software Testing in JSON Format", "url": "http://www.test.org/stable/20.1.2.3.5", "volumeNumber": 15, "wordCount": 2000, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "article", "subTitle": "A Comprehensive Review", "abstract": "Another abstract"},
            {"creator": ["Saif Tested"], "datePublished": "2017-04-02", "docType": "document", "doi": "20.1.2.3.6", "id": "http://www.test.org/stable/20.1.2.3.6", "identifier": [{"name": "doi", "value": "20.1.2.3.6"}, {"name": "issn", "value": "201236"}, {"name": "oclc", "value": "201236"}, {"name": "lccn", "value": "201236"}, {"name": "local_uuid", "value": "201236-jjjjj"}], "isPartOf": "Testing Today", "issueNumber": 2, "keyphrase": ["software testing", "examples"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 10, "pageEnd": 90, "pageStart": 80, "pagination": "pp. 80-90", "provider": "jstor", "publicationYear": 2017, "publisher": "Fake Publisher", "sourceCategory": ["Software"], "tdmCategory": ["Technology"], "title": "Testing", "url": "http://www.test.org/stable/20.1.2.3.6", "volumeNumber": 8, "wordCount": 500, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "article", "subTitle": "Key Developments 2017", "abstract": "The third abstract"}
            ]
        with open(f'{CURRENT_DIR}/test_data/test_data1.jsonl', 'w') as file_:
            for item in data_as_dicts:
                file_.write(json.dumps(item) + "\n")

        undertest = DataHandler(paths_to_data = [f'{CURRENT_DIR}/test_data/test_data1.jsonl'])

        # when - we call the load data method
        actual_df = undertest._load_data()
        expected_df = pd.DataFrame.from_dict(data_as_dicts)
        # then - the under test instance has an attribute self.json_df
        self.assertTrue(hasattr(undertest, 'json_df'))

    def test_load_data_returns_df_with_expected_data_from_multiple_files(self):
        # given - a data handler instance reading in two files of data with know values
        data_as_dicts1 = [
            {"creator": ["Michael Test"], "datePublished": "2013-04-01", "docType": "document", "doi": "20.1.2.3.4", "id": "http://www.test.org/stable/20.1.2.3.4", "identifier": [{"name": "doi", "value": "20.1.2.3.4"}, {"name": "issn", "value": "201234"}, {"name": "oclc", "value": "201234"}, {"name": "lccn", "value": "201234"}, {"name": "local_uuid", "value": "201234-hhhhhhh"}], "isPartOf": "Journal of Testing", "issueNumber": 1, "keyphrase": ["testing", "test"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 1, "pageEnd": 100, "pageStart": 100, "pagination": "pp. 100", "provider": "jstor", "publicationYear": 2013, "publisher": "Test Press", "sourceCategory": ["Test"], "tdmCategory": ["Technology"], "title": "Testing - A JSONL object", "url": "http://www.test.org/stable/20.1.2.3.4", "volumeNumber": 10, "wordCount": 100, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "review", "subTitle": "An Analysis of Testing Methods", "abstract": "An abstract"},
            {"creator": ["Samira Tester"], "datePublished": "2015-04-02", "docType": "document", "doi": "20.1.2.3.5", "id": "http://www.test.org/stable/20.1.2.3.5", "identifier": [{"name": "doi", "value": "20.1.2.3.5"}, {"name": "issn", "value": "201235"}, {"name": "oclc", "value": "201235"}, {"name": "lccn", "value": "201235"}, {"name": "local_uuid", "value": "201235-iiiii"}], "isPartOf": "Testing Today", "issueNumber": 2, "keyphrase": ["software testing", "data"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 20, "pageEnd": 100, "pageStart": 80, "pagination": "pp. 80-100", "provider": "jstor", "publicationYear": 2015, "publisher": "Testing Example", "sourceCategory": ["Example"], "tdmCategory": ["Technology"], "title": "Software Testing in JSON Format", "url": "http://www.test.org/stable/20.1.2.3.5", "volumeNumber": 15, "wordCount": 2000, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "article", "subTitle": "A Comprehensive Review", "abstract": "Another abstract"},
            {"creator": ["Saif Tested"], "datePublished": "2017-04-02", "docType": "document", "doi": "20.1.2.3.6", "id": "http://www.test.org/stable/20.1.2.3.6", "identifier": [{"name": "doi", "value": "20.1.2.3.6"}, {"name": "issn", "value": "201236"}, {"name": "oclc", "value": "201236"}, {"name": "lccn", "value": "201236"}, {"name": "local_uuid", "value": "201236-jjjjj"}], "isPartOf": "Testing Today", "issueNumber": 2, "keyphrase": ["software testing", "examples"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 10, "pageEnd": 90, "pageStart": 80, "pagination": "pp. 80-90", "provider": "jstor", "publicationYear": 2017, "publisher": "Fake Publisher", "sourceCategory": ["Software"], "tdmCategory": ["Technology"], "title": "Testing", "url": "http://www.test.org/stable/20.1.2.3.6", "volumeNumber": 8, "wordCount": 500, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "article", "subTitle": "Key Developments 2017", "abstract": "The third abstract"}
            ]
        with open(f'{CURRENT_DIR}/test_data/test_data1.jsonl', 'w') as file_:
            for item in data_as_dicts1:
                file_.write(json.dumps(item) + "\n")

        data_as_dicts2 = [
            {"creator": ["Example Author"], "datePublished": "2013-06-01", "docType": "document", "doi": "20.1.2.3.8", "id": "http://www.test.org/stable/20.1.2.3.8", "identifier": [{"name": "doi", "value": "20.1.2.3.8"}, {"name": "issn", "value": "201238"}, {"name": "oclc", "value": "201238"}, {"name": "lccn", "value": "201234"}, {"name": "local_uuid", "value": "201234-hhhhhhh"}], "isPartOf": "Journal of Testing", "issueNumber": 1, "keyphrase": ["testing", "test"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 1, "pageEnd": 100, "pageStart": 100, "pagination": "pp. 100", "provider": "jstor", "publicationYear": 2013, "publisher": "Test Press", "sourceCategory": ["Test"], "tdmCategory": ["Technology"], "title": "Testing - A JSONL object", "url": "http://www.test.org/stable/20.1.2.3.4", "volumeNumber": 10, "wordCount": 100, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "review", "subTitle": "An Analysis of Testing Methods", "abstract": "An abstract"},
            {"creator": ["Fictional Writer"], "datePublished": "2015-04-02", "docType": "document", "doi": "20.1.2.3.9", "id": "http://www.test.org/stable/20.1.2.3.5", "identifier": [{"name": "doi", "value": "20.1.2.3.5"}, {"name": "issn", "value": "201235"}, {"name": "oclc", "value": "201235"}, {"name": "lccn", "value": "201235"}, {"name": "local_uuid", "value": "201235-iiiii"}], "isPartOf": "Testing Today", "issueNumber": 2, "keyphrase": ["software testing", "data"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 20, "pageEnd": 100, "pageStart": 80, "pagination": "pp. 80-100", "provider": "jstor", "publicationYear": 2015, "publisher": "Testing Example", "sourceCategory": ["Example"], "tdmCategory": ["Technology"], "title": "Software Testing in JSON Format", "url": "http://www.test.org/stable/20.1.2.3.5", "volumeNumber": 15, "wordCount": 2000, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "article", "subTitle": "A Comprehensive Review", "abstract": "Another abstract"},
            {"creator": ["Sample Scribe"], "datePublished": "2017-04-02", "docType": "document", "doi": "20.1.2.3.10", "id": "http://www.test.org/stable/20.1.2.3.6", "identifier": [{"name": "doi", "value": "20.1.2.3.6"}, {"name": "issn", "value": "201236"}, {"name": "oclc", "value": "201236"}, {"name": "lccn", "value": "201236"}, {"name": "local_uuid", "value": "201236-jjjjj"}], "isPartOf": "Testing Today", "issueNumber": 2, "keyphrase": ["software testing", "examples"], "language": ["en"], "outputFormat": ["unigrams", "bigrams", "trigrams", "bigram", "trigram"], "pageCount": 10, "pageEnd": 90, "pageStart": 80, "pagination": "pp. 80-90", "provider": "jstor", "publicationYear": 2017, "publisher": "Fake Publisher", "sourceCategory": ["Software"], "tdmCategory": ["Technology"], "title": "Testing", "url": "http://www.test.org/stable/20.1.2.3.6", "volumeNumber": 8, "wordCount": 500, "unigramCount": {}, "bigramCount": {}, "trigramCount": {}, "docSubType": "article", "subTitle": "Key Developments 2017", "abstract": "The third abstract"}
            ]
        with open(f'{CURRENT_DIR}/test_data/test_data2.jsonl', 'w') as file_:
            for item in data_as_dicts2:
                file_.write(json.dumps(item) + "\n")

        undertest = DataHandler(paths_to_data = [f'{CURRENT_DIR}/test_data/test_data1.jsonl', f'{CURRENT_DIR}/test_data/test_data2.jsonl'])
        data_as_dicts1.extend(data_as_dicts2)
        # when - we call the load data method
        actual_df = undertest._load_data()
        expected_df = pd.DataFrame.from_dict(data_as_dicts1)
        # then - a dataframe version of the combined data is returned
        assert_frame_equal(actual_df, expected_df)

    # == TEST REMOVE COLUMNS == #

    def test_remove_columns_removes_the_expected_columns_and_returns_updated_df(self):
        # given - an instance of the undertest data handler reading in some data
        undertest = DataHandler(paths_to_data = [f'{CURRENT_DIR}/test_data/test_data1.jsonl', f'{CURRENT_DIR}/test_data/test_data2.jsonl'])
        
        # when - we call the remove columns method passing in some columns to remove
        actual_df = undertest._remove_columns(['docType', 'doi', 'unigramCount', 'bigramCount', 'trigramCount', 'creator', 'volumeNumber'])
        actual_columns = sorted(actual_df.columns)
        expected_columns = sorted(['datePublished', 'docSubType', 'id', 'identifier', 'isPartOf', 'issueNumber', 'language', 'outputFormat', 'pageCount', 'pageEnd', 'pageStart', 'pagination', 'provider', 'publicationYear', 'publisher', 'sourceCategory', 'tdmCategory', 'title', 'url', 'wordCount', 'subTitle', 'abstract', 'keyphrase'])

        # then - the dataframe returned doesn't have the removed columns
        self.assertListEqual(actual_columns, expected_columns)

    def test_remove_columns_updates_the_json_df_class_attr_with_new_columns(self):
        # given - an instance of the undertest data handler reading in some data
        undertest = DataHandler(paths_to_data = [f'{CURRENT_DIR}/test_data/test_data1.jsonl', f'{CURRENT_DIR}/test_data/test_data2.jsonl'])
        
        # when - we call the remove columns method passing in some columns to remove
        actual_df = undertest._remove_columns(['docType', 'doi', 'unigramCount', 'bigramCount', 'trigramCount', 'creator', 'volumeNumber'])
        actual_columns = sorted(undertest.json_df.columns)
        expected_columns = sorted(['datePublished', 'docSubType', 'id', 'identifier', 'isPartOf', 'issueNumber', 'language', 'outputFormat', 'pageCount', 'pageEnd', 'pageStart', 'pagination', 'provider', 'publicationYear', 'publisher', 'sourceCategory', 'tdmCategory', 'title', 'url', 'wordCount', 'subTitle', 'abstract', 'keyphrase'])

        # then - the dataframe in the class attribute doesn't have the removed columns
        self.assertListEqual(actual_columns, expected_columns)

    # == TEST LOAD MODEL == #

    # NOTE: multiple assertions in one test case as this takes a few secs
    def test_load_model_returns_sets_model_and_tokenizer_as_class_attr(self):
        # given - an instance of the undertest data handler
        undertest = DataHandler(paths_to_data = [f'{CURRENT_DIR}/test_data/test_data1.jsonl'])

        # when - we call the load model method
        actual_model = undertest._load_model()

        # then - the undertest instance has the expected model and tokenizer attributes
        self.assertTrue(hasattr(undertest, 'model'))
        self.assertTrue(hasattr(undertest, 'tokenizer'))

    # == TEST EMBED ENTRY == #

    # NOTE: will differ by model!
    def test_embed_entry_returns_expected_type_and_dimensions(self):
        # given - an instance of the undertest data handler and a string to embed
        undertest = DataHandler(paths_to_data = [f'{CURRENT_DIR}/test_data/test_data1.jsonl'])
        string_to_embed = "JSTOR is a fantastic resource for open access academic materials"

        # when - we call the embed entry method
        actual_embedding = undertest._embed_entry(string_to_embed)
        expected_len = 768

        # then - the embedding returned is a list of floats with the expected dimensions for the current model
        self.assertTrue(type(actual_embedding) == list)
        self.assertTrue(all(type(i) == float for i in actual_embedding))
        self.assertEqual(len(actual_embedding), expected_len)

    # == TEST RUN == #

    def test_run_creates_attrs_from_loading_model_and_data(self):
        # given - an instance of the undertest data handler
        undertest = DataHandler(paths_to_data = [f'{CURRENT_DIR}/test_data/test_data1.jsonl'])

        # when - we call the run method
        undertest.run()

        # then - the undertest instance has the expected model, tokenizer and data attributes
        self.assertTrue(hasattr(undertest, 'model'))
        self.assertTrue(hasattr(undertest, 'tokenizer'))
        self.assertTrue(hasattr(undertest, 'json_df'))