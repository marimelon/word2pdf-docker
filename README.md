# word2pdf-api

This container runs a web service that converts Japanese Word files to PDF using LibreOffice.

## Usage

### Build

    docker build -t word2pdf-api .

### Run

    docker run -it --rm -p 8000:80 word2pdf-api

### Convert file

    curl -F file=@filename http://127.0.0.1:8000 -o out.pdf
