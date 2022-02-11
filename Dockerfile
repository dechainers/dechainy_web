# Copyright 2022 DeChainers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Supported "latest", "test" and "ml-cpu"
ARG BASE_IMAGE_BUILDTAG="latest"
FROM s41m0n/dechainy_web:$BASE_IMAGE_BUILDTAG

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python3", "-W ignore", "-m dechainy_web"]

#######################
# docker run --rm -it --privileged --network host
#   -v /lib/modules:/lib/modules:ro \
#   -v /usr/src:/usr/src:ro \
#   -v /etc/localtime:/etc/localtime:ro 
#   s41m0n/dechainy_web:<tag> <your_python_code>
#######################
# To build for arm64 from a non-arm device
#
# docker buildx build -f Dockerfile -t s41m0n/dechainy_web:arm --platform linux/arm64 . --load 
#######################