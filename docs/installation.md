# Installation

## Requirements

The project comes with a quick and easy to build Docker image, which can be built and used in less than a minute.
Although, for those who does not want to use the image and run the module locally, the requirements are:

* requirements.txt
* python3-pytest (only if testing)

Please refer to the DeChainy [installation guide](https://github.com/dechainers/dechainy/blob/master/docs/installation.md) as there are all the indications to correctly build the previous requirements.

## Install

### Local

```bash
# Installing other dependencies
sudo apt install python3-pytest
sudo pip3 install -r requirements.txt
sudo python3 -m dechainy_web
```

If you want to install DeChainyWeb as a Python package, after satisfying the BCC dependency, you can use the [setup.py](../setup.py) script:

```bash
sudo python3 setup.py install
```

From now on, you can reference to this framework as you would do for any other Python package, like *import numpy*.

### Docker

```bash
docker build -f Dockerfile -t s41m0n/dechainy_web:latest .
```

```bash
docker run --rm --privileged --network host \
    -v /lib/modules:/lib/modules:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v /usr/src:/usr/src:ro \
    -v $(pwd)/dechainy_web:/app/:ro \ # you can mount at runtime the new code you develop, instead of rebuilding it
    -v $(pwd)/startup.json:/app/startup.json:ro \ # or you can just mount only the startup configuration
    s41m0n/dechainy_web:latest
```

If you are willing to use TensorFlow or Keras, the main [Dockerfile](../Dockerfile) accepts an additional
parameter to include such additional packages:

```bash
docker build --build-arg DEFAULT_BUILDTYPE=ml -t s41m0n/dechainy_web:ml-cpu .
```

Finally, if you want to exploit your GPU usage, you should use the [Dockerfile.gpu](../Dockerfile.gpu) file.

```bash
docker build -f Dockerfile.gpu -t s41m0n/dechainy_web:ml-gpu .
```
