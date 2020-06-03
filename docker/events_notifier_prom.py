#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Clustree <https://www.clustree.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
import docker
from prometheus_client import start_http_server, Counter

APP_NAME = "Docker events prometheus exporter"
EVENTS = Counter('docker_events',
                 'Docker events',
                 ['event', 'type', 'image', 'name'])


def watch_events():
    client = docker.DockerClient(version='auto',
                                 base_url='unix://var/run/docker.sock')
    for event in client.events(decode=True):
        type_event = event['Type']
        try:
            actor = event['Actor']
            attributes = actor['Attributes']
            event = event['status'].strip()
            EVENTS.labels(event=event, type=type_event, image=attributes['image'], name=attributes['name']).inc()
        except Exception as e:
            print(event)
            pass


if __name__ == '__main__':
    start_http_server(9000, addr='0.0.0.0')
    try:
        watch_events()
    except docker.errors.APIError:
        pass
