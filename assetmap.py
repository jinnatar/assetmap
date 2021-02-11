import json

from absl import flags
from absl import logging
from absl import app

from form2enum import form2enum

FLAGS = flags.FLAGS

flags.DEFINE_string('game_master', 'V2_GAME_MASTER.json', 'path to V2_GAME_MASTER.json')

def is_form(item):
    if 'formSettings' in item[1]['data'] and 'forms' in item[1]['data']['formSettings']:
        return True
    else:
        return False



def make_forms(gm=None):
    if gm == None:
        with open(FLAGS.game_master, 'r') as f:
            gm = json.load(f)

    # move from the list format of the gm to a simple dict
    master_dict = {item['templateId']:item for item in gm['template']}
    # Drop useless levels and items
    forms_dict = {item[1]['data']['formSettings']['pokemon']:item[1]['data']['formSettings']['forms']
            for item in master_dict.items() if is_form(item)}
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
        asset_name = formname(form)
        logging.debug('{}:{} ({})'.format(form_id, asset_id, asset_name))
        full_map[form_id] = {
                'asset_id': asset_id,
                'asset_name': asset_name
                }
    print(json.dumps(full_map, indent=2, sort_keys=True))

def formname(enum):
    form = enum.split('_', 1)[1] # prune name from front
    form = form.replace('_', ' ') # replace further breaks with spaces
    return form.capitalize()

def main(argv):
    del argv
    make_full_map()

if __name__ == '__main__':
    app.run(main)
