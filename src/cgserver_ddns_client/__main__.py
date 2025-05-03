#!/usr/bin/env python3
from cgserver_ddns_client import clienttask
from urllib import request, parse
import sys
from pydantic import BaseModel
import json


class Config(BaseModel):
    url: str
    client_id: str
    client_secret: str


if __name__ == "__main__":
    config = Config.model_validate_json(sys.stdin.read())
    url: str = config.url
    report = clienttask.alltasks()
    data = dict(
        client_id=config.client_id,
        client_secret=config.client_secret,
        report=json.dumps(report),
    )
    request = request.urlopen(url, parse.urlencode(data).encode("utf-8"))
    assert 200 == request.code
    content = request.read().decode("utf-8")
    print(content)
