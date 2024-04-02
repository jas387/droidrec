# A droidrec Flet app
android record utility interface for scrcpy

# How-To setup

Create and change to project directory (DroidRec/src):

```
mkdir -pv DroidRec/src
cd DroidRec
```

Clone this repo in src:

```
gh repo clone jas387/droidrec src/
```

Make virtual enviroment and activate:

```
python -m venv venv
source venv/bin/activate
```



Install deps:

```
pip install -r src/requirements.txt
```

To run the app:

```
flet run src
```