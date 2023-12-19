# spotify_music_recommender 

By: Brayam Pineda.

Version: 0.1.0

In this project I'll create a music recommender in Spotify via OpenAI. This will be great, cause will connect to Spotify API

## Create environment

```bash
conda env create -f environment.yml
activate spotify_music_recommender
```

or 

```bash
mamba env create -f environment.yml
activate spotify_music_recommender
```

## Project organization

    spotify_music_recommender
        ├── data
        │   ├── processed      <- The final, canonical data sets for modeling.
        │   └── raw            <- The original, immutable data dump.
        │
        ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
        │                         the creator's initials, and a short `-` delimited description, e.g.
        │                         `1.0-initial-data-exploration`.
        │
        ├── .gitignore         <- Files to ignore by `git`.
        │
        ├── environment.yml    <- The requirements file for reproducing the analysis environment.
        │
        └── README.md          <- The top-level README for developers using this project.

---
