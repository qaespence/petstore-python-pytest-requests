# petstore-python-pytest-requests
Swagger PetStore API testing framework, written in Python, using Pytest and Requests

## Testing
### Installation

1. Install Python (if not already installed).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Tests

Run the tests using pytest:

```bash
pytest
```

### Folder Structure

Here’s a description of the project’s folder and file structure:
```
.
├── test/                       # Main test folder containing all test-related files
│   ├── api/                    # Contains API request functions (e.g., addPet, getPet, updatePet, deletePet)
│   │   ├── basicRequests.py    # Contains core request methods (POST, GET, PUT, DELETE)
│   │   └── schemaDB.json       # Expected schema responses
│   ├── config/                 # Contains config files
│   │   └── config.json         # Config settings (mainly base_url)
│   ├── helpers/                # Contains utility functions
│   │   └── utils.py            # Utility functions (e.g., logging, clearing logs, etc.)
│   ├── logs/                   # Stores log files for each test suite
│   └── specs/                  # Contains all the test cases for different API endpoints
│       └── test_pet.py         # Test cases for the Pet API endpoints
├── .gitignore                  # Files and folders to ignore in Git
├── requirements.txt            # Project dependencies and scripts
└── README.md                   # Project instructions and documentation (this file)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
