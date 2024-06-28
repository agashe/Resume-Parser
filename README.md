# Resume Parser

A very simple resume parser , that fetch basic information from resume and then format it into JSON payload, the extracted information including :

* Personal / Contact
* Skills
* Experience
* Education
    
So far this program is very limited , since it doesn't depend on any NLP solution , so it's very basic.

## Documentation

### Installation

To start using this program , we start by installing all required dependencies , by running the following command in the terminal :

First we create new virtual environment :

```
python3 -m venv env
```

Then we start the installation :

```
pip install -r requirements.txt 
```

### Usage

The Resume-Parser provides 3 arguments :

```
-h, --help                  show this help message and exit
-f FILE, --file FILE      The path to the resume
-o FILE, --output FILE    The path to the output json file
```

The `--output` argument is optional , and in this case the parser will just print the JSON payload into the terminal.

### Example

In the following example , we provide the resume `test_3.pdf` and write the output into the `data.json` file.

```
python3 src/resume_parser.py -f tests/test_3.pdf -o dist/data.json
```
And the same command can be written without the JSON output file :

```
python3 src/resume_parser.py -f tests/test_3.pdf
```

## License

(Resume Parser) released under the terms of the MIT license.
