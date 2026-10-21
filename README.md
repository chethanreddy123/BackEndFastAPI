# Insurance keyword recommendation API

A historical team prototype that helps a user turn a short insurance query into related search terms and product links. The backend combines autocomplete, text classification and similarity matching behind a FastAPI endpoint.

This repository preserves the original implementation and model artifacts. It is useful for reviewing the API and retrieval design; it is not presented as a maintained production service or a measured search-quality benchmark.

## Request flow

```text
POST /getInformation
  → read SearchedString
  → autocomplete against the saved vocabulary
  → predict an insurance category with the saved classifier
  → load that category's keyword CSV
  → select related terms
  → return up to 10 results
```

The implementation is in [main.py](main.py):

- `fast-autocomplete` chooses the first suggestion with edit cost at most 2.
- `model_joblib` predicts the category used to select a CSV file.
- Most categories use cosine similarity over token-count vectors, with a `> 0.3` threshold. Health queries return the category's terms without that similarity filter.
- Successful responses contain `SearchResults`, a list of objects with `text`, `link` and `type` fields.

The [analysis notebook](ML-Algo-Analysis.ipynb) explores count/TF-IDF features, a hinge-loss SGD classifier and Multinomial Naive Bayes. Its final `joblib.dump` cell saves the Naive Bayes pipeline. The notebook is an exploratory record, not a clean, deterministic training pipeline, and no accuracy figure is asserted here.

## Repository map

| File | Purpose |
|---|---|
| [main.py](main.py) | FastAPI application, classification, category selection and result assembly |
| [automata.py](automata.py) | Interactive autocomplete experiment with an edit-cost limit of 3 |
| `sample.pkl` | Serialized autocomplete vocabulary, loaded when the application is imported |
| `model_joblib` | Serialized classifier, loaded during a request |
| `*Keywords*.csv`, `Commercial.csv`, `cyber.csv` | Category keyword lists; the API expects a `SearchedWord` column |
| [ML-Algo-Analysis.ipynb](ML-Algo-Analysis.ipynb) | Historical data preparation and classifier experiments |
| [requirements.txt](requirements.txt) | Historical dependency pins |
| [runtime.txt](runtime.txt), [Procfile](Procfile) | Original Python 3.8.5 / Gunicorn-Uvicorn deployment configuration |

## Local reproduction

The recorded runtime is **Python 3.8.5**. Use an isolated environment for this historical stack. Dependency installation and serialized-model compatibility have not been revalidated on current Python versions.

```bash
git clone https://github.com/chethanreddy123/BackEndFastAPI.git
cd BackEndFastAPI
python3.8 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Run from the repository root: the vocabulary, model and CSV paths are relative to the working directory. Use only artifacts whose provenance you trust; Python pickle/joblib loading can execute code. The API does not require a cloud API key or database connection.

After successful startup, open [the local API documentation](http://127.0.0.1:8000/docs) or send a request:

```bash
curl --request POST http://127.0.0.1:8000/getInformation \
  --header 'Content-Type: application/json' \
  --data '{"SearchedString":"car insurance"}'
```

Successful response shape, with illustrative values rather than a verified prediction:

```json
{
  "SearchResults": [
    {
      "text": "<suggested keyword>",
      "link": "<category product URL>",
      "type": "<predicted category>"
    }
  ]
}
```

## Engineering boundaries

- The request body is read directly rather than validated with a typed schema. Missing fields, invalid JSON and empty autocomplete results are not handled as clean API errors.
- The classifier and CSV are loaded on each request. Caching, concurrency behavior and latency have not been benchmarked.
- The notebook prepares a five-category training subset; the API contains nine category branches. Rebuilding the model requires reconciling that training coverage with the runtime category IDs.
- CORS is permissive, request bodies are printed, and there is no authentication or rate limiting. Those are changes needed before exposing this prototype as a public service.
- Product URLs are hard-coded historical links, including advertising redirects. Their availability and suitability are not guaranteed by the API.
- There is no automated application test suite or CI workflow in this repository. A documentation review on 21 October 2026 checked Python syntax, file references and CSV headers; it did not start the API, deserialize model artifacts or validate predictions.

## Original project material

[Historical frontend](https://key-n-surance.netlify.app/) — availability was not confirmed in the documentation review.

### Solution overview

![Original team solution diagram](https://user-images.githubusercontent.com/69640722/182427360-4bacc3d5-15ef-44af-85e7-18d8cb6de475.jpg)

### Sample interface

![Original search-results interface](https://user-images.githubusercontent.com/69640722/182427454-d9f32efd-d3c7-4563-bdd4-6eb2ba986a2c.jpg)

This was a team project. The repository documents the implementation available here without assigning every component to one contributor.
