#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
from datetime import datetime
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
import subprocess
import platform
import re
import torch


def kill_port(port: int) -> str:
    print (port)

if __name__ == "__main__":

    kill_port (11434)

    print(torch.__version__, torch.backends.mps.is_available())
