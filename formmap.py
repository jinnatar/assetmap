import json

from absl import flags
from absl import logging
from absl import app

from form2enum import form2enum

FLAGS = flags.FLAGS


def make_form_map():
    print(json.dumps(form2enum, indent=2, sort_keys=True))


def main(argv):
    del argv
    make_form_map()

if __name__ == '__main__':
    app.run(main)
