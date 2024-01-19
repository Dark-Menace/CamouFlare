
# CamouFlare

The Steganography Tool is a versatile project that combines the power of a Command Line Interface (CLI) and a Web User Interface (WebUI) to enable users to seamlessly embed and extract hidden data within images. Steganography is the art and science of concealing information within seemingly innocuous media to protect the confidentiality and integrity of data.


## Installation

Clone the project

```bash
  git clone https://github.com/Dark-Menace/CamouFlare.git
```

Go to the project directory

```bash
  cd CamouFlare
```
Install dependencies

```bash
  pip install -r requirements.txt
```




## Usage


#### CLI : ####

Go to the CLI directory:

```bash
  cd CLI
```

Run the steganography script:

```bash
  python camouflare.py
```

***

#### MyFlaskApp : ####

Go to the CLI directory:

```bash
  cd MyFlaskApp
```
Run the flask server :

```bash
  flask run
```

#### Opening in browser : ####

On Linux:

```bash
  xdg-open http://localhost:5000
```

On macOS:

```bash
  open http://localhost:5000
```

On Linux:

```bash
  start http://localhost:5000
```
If you are running the flask server on another remote machine, change the http request url in the "script.js" file present in the "static" directory.
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Disclaimer

This tool is for educational purposes only. Use responsibly and ensure compliance with applicable laws and regulations.
