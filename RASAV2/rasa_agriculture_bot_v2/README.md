# Agriculture Chatbot with RASA

This repository contains a fully functional RASA chatbot module for agriculture, designed to provide information about various crops, their diseases, pests, fertilizer requirements, and more.

## Project Structure

```
rasa_agriculture_bot_v2/
├── actions/
│   └── actions.py           # Custom actions for slot filling and form handling
├── data/
│   ├── nlu/
│   │   ├── agriculture.yml  # Agriculture-specific NLU training data
│   │   └── general.yml      # General conversation NLU training data
│   ├── rules/
│   │   └── rules.yml        # Rules for conversation flows
│   └── stories/
│       └── stories.yml      # Stories for conversation flows
├── tests/
│   └── test_rasa_files.py   # Tests for validating RASA files
├── config.yml               # NLU pipeline and policy configuration
├── credentials.yml          # Channel credentials configuration
├── domain.yml               # Domain specification with intents, entities, slots, and responses
├── endpoints.yml            # Endpoints configuration for action server
└── requirements.txt         # Python dependencies
```

## Features

- Intent classification for 30+ agriculture-related intents
- Entity extraction for crops and varieties
- Form-based slot filling for missing information
- Custom actions for handling agriculture-specific queries
- Comprehensive responses for various agricultural topics

## Installation

1. Create a virtual environment:

```bash
python -m venv ./venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows
```

2. Install the required dependencies:

```bash
pip install -r requirements_final.txt
```

## Training the Model

To train the RASA model:

```bash
rasa train
```

This will create a model in the `models/` directory.

## Running the Bot

1. Start the action server (in a separate terminal):

```bash
rasa run actions
```

2. Start the RASA server:

```bash
rasa run --enable-api --cors "*"
```

3. For better Visualaization:

```bash
rasa interactive -p 5056
```


4. For interactive testing in the command line:

```bash
rasa shell
```

## Testing

To validate the RASA data files:

```bash
rasa data validate
```





### Debugging Tips

- Use `rasa shell --debug` to see detailed logs during conversation
- Check the action server logs for any errors in custom actions
- Use `rasa interactive` to test and correct conversation flows

## Extending the Bot

### Adding New Intents

1. Add new intent examples to `data/nlu/agriculture.yml`
2. Update the domain.yml file to include the new intent
3. Add appropriate responses in domain.yml
4. Update the ActionSetRequestedInfo class in actions.py
5. Create stories and rules for the new intent

### Adding New Entities

1. Add entity examples in the NLU data
2. Add the entity to domain.yml
3. Update the form validation in actions.py

## License

This project is open-source and available for use and modification.
