import json

from absl import flags
from absl import logging
from absl import app

from form2enum import form2enum

FLAGS = flags.FLAGS

flags.DEFINE_string('game_master', 'GAME_MASTER.json', 'path to GAME_MASTER.json')

def make_forms(gm=None):
    if gm == None:
        with open(FLAGS.game_master, 'r') as f:
            gm = json.load(f)

    # move from the list format of the gm to a simple dict
    master_dict = {item['templateId']:item for item in gm['itemTemplates']}
    # Drop useless levels and items
    forms_dict = {item[1]['formSettings']['pokemon']:item[1]['formSettings']['forms']
            for item in master_dict.items()
            if 'formSettings' in item[1]
            and 'forms' in item[1]['formSettings']}

    forms = {}
    # Simplify structure to just form:asset_id pairs
    for formlist in forms_dict.values():
        for form in formlist:
            if 'assetBundleValue' in form:
                forms[form['form']] = '{:02d}'.format(form['assetBundleValue'])
            elif 'assetBundleSuffix' in form:
                forms[form['form']] = form['assetBundleSuffix']
            else:
                logging.debug('no asset found for {}'.format(form))
    return forms


def form2asset(enum, forms):
    if enum in forms:
        return forms[enum]
    else:
        return '00'


def make_full_map():
    forms = make_forms()
    full_map = {}
    for form_id, form in form2enum.items():
        asset_id = form2asset(form, forms)
        logging.debug('{}:{}'.format(form_id, asset_id))
        full_map[form_id] = asset_id
    print(json.dumps(full_map, indent=2, sort_keys=True))


def main(argv):
    del argv
    make_full_map()

if __name__ == '__main__':
    app.run(main)
