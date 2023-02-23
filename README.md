# Tyrion Lannister Chatbot
This chatbot (sometimes) has the personality of Tyrion Lannister from Game of Thrones. He is a witty, intelligent and zynical dwarf and one of the main characters of the show. He likes to have a drink or two, but you might figure that out for yourself.

## Data
The Tyrion Lannister chatbot is based on the following corpora with request-reply pairs:
- ~ 1.300 [Tyrions dialogs from the tv show](https://genius.com/artists/Game-of-thrones)
- ~ 210.000 [cornell movie-dialogs corpus](https://convokit.cornell.edu/documentation/movie.html)
- ~ 86.000 [daily-dialogs](http://yanran.li/dailydialog.html)

Additionally ~1.000 patternbased answers cover some more specific user inputs such as greetings, exchanging names and saying goodbye.

## Environment
Choose one way to initialize your environment:

### 1. Conda Environment

```
conda env create -f environment.yml
```

```
conda activate Chatbot
```

### 2. pip Environment

```
pip install -r requirements.txt
```

## Preprocessing
You need to preprocess the data in order to use the Tyrion chatbot. Execute the following:

```
python preprocessing.py --use_preset
```

You can choose different configurations for the preprocessing. Here is a list of all possible configurations with a short explanation: 

| Argument | Explanation |
| - | - |
| `--data_path` |  |
| `--keep_prior_data` | Does not delete previously preprocessed data. |
| `--use_preset` | Preprocesses the Preset Corpora set by developer. |
| `--with_all` | Preprocess all types of corpora. |
| `--with_got` | Preprocess the got transcripts. |
| `--with_cornell` | Preprocess the cornell movie-dialogs corpus. |
| `--with_parliament` | Preprocess the Parliament Question Time Corpus. |
| `--with_daily` | Preprocess the Daily Dialogs Corpus. |


## Start the chatbot
You can start the Tyrion chatbot by executing the following command:

```
python live_demo.py
```

The chatbot will ask if you want to connect to establish a connection to the other chatbots or if you want to use the normal chatting mode. After entering 'yes' or 'no' you are **ready to go**!




