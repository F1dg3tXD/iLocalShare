# iLocalShare  

A simple, no-frills local file-sharing server. Works between Windows and iOS (or anything with a browser, really). Built in about 20 minutes because AirDrop refuses to cooperate with non-Apple devices. 

<b>Fuck you Tim.</b> 

<img src="icon.png" alt="iFileShare" width="300"/>

## Features  

✅ Drag-and-drop file uploads  
✅ Web-based frontend (so you don’t need extra apps)  
✅ Open-access and password-protected modes  
✅ Works on anything with a browser  

## Installation  

1. Install **Python 3.11.3** (or the latest version that works).  
   - [Download Python](https://www.python.org/downloads/) if you don’t have it.  

2. Clone this repo or download the files manually.  

3. Install dependencies:  

   ```
   pip install -r requirements.txt

## Usage
### Option 1: Open Server (No Password)
For when you trust everyone on your network (or just don’t care).

```
python server.py
```
This starts a local server that anyone can access.

### Option 2: Secure Server (With Password)
For when you realize that trusting everyone is a bad idea.

```
python secure-server.py
```
This will prompt you to set a password, required for file access.

## Accessing the Web App
Open a browser on your phone or computer.

Go to <http://your-pc-ip:5000>.

Start sharing files.

## Building Executable
 * Make sure `build.spec` is configured to your liking.
 * Run `pyinstaller build.spec`

## TODO
* Secure server password handling needs remaking for tray application. (not working)


# Why This Exists
Because sometimes, you just need to move a file from point A to point B without Apple, Microsoft, or some over-engineered cloud service getting in the way.

