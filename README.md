## INTRODUCTION
General python yolo framework, warp of [pyyolo](https://github.com/thomaspark-pkj/pyyolo.git
), including training and inference processes.

## CREATE VIRTUAL ENV
create python3 virtual env:

```
virtualenv -p python3 --no-site-packages venv
```

activate virtual env:

```
source venv/bin/activate
```

## INSTALL requirements
```
pip install -r requirements.txt
```

## INSTALL pyyolo
clone project:

```
git clone --recursive https://github.com/thomaspark-pkj/pyyolo.git
```

Delete line 170 in module.c, then follow pyyolo README.md


## PREPARATION
```
cd gpyyolo
cp conf.json.tmpl conf.json
cp ../cfg/* ../pyyolo/darknet/cfg
```
make sure that model weight file is in dir: pyyolo/


## RUN
### INFERENCE
```
cd gpyyolo
python gpyyolo.py -task inference
```