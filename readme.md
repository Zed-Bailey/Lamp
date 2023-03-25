# Lamp


create .env file
```env
    PICO_CONSOLE_KEY="[access key, can be found in picovoice console]"
    RHINO_CONTEXT_FILE="[.rhn file path]"
    PORCUPINE_KEYWORD_FILE="[.ppn file]"
```

default porcupine wakeword files can be found here: https://github.com/Picovoice/porcupine/tree/0c179e7d3cb3b9dff762df5d0d1132709611fa5f/resources
default rhino context files can be found here: https://github.com/Picovoice/rhino/tree/5c42e5629925d91645aea51f93fedf7b36b160a4/resources

## libraries
- opencv-python
- picovoice
- pvrecorder
- python-dotenv