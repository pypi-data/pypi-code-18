"""Method to read information about available models and parameters from the
current SCO code. Store information in database for Web API and UI.
"""

import json
import sco
import sys

if len(sys.argv) != 3:
    print 'Usage: <models-output-file> <image-group-parameters-output-file>'
    sys.exit()

f_models = sys.argv[1]
f_image_groups = sys.argv[2]

IMG = [
    'aperture_edge_width',
    'aperture_radius',
    'background',
    'pixels_per_degree',
    'gamma'
]

MOD = [
    'compressive_constants_by_label',
    'contrast_constants_by_label',
    'divisive_exponents_by_label',
    'gabor_orientations',
    'max_eccentricity',
    'modality',
    'normalized_pixels_per_degree',
    'pRF_n_radii',
    'pRF_sigma_slopes_by_label',
    'saturation_constants_by_label'
]


models = []
img_group_parameters = []
igp_index = set()

for m_name in sco.model_names():
    model = {'id' : m_name, 'name' : m_name, 'description' : ''}
    parameters = []
    model['parameters'] = parameters
    models.append(model)
    m = sco.build_model(m_name, force_exports=False)
    for p_name in m.afferents:
        if p_name in IMG or p_name in MOD:
            para = {'id' : p_name, 'name' : p_name}
            para['description'] = m.afferent_docs[p_name]
            if p_name in m.defaults:
                def_value = str(m.defaults[p_name])
                if def_value.startswith('pmap('):
                    def_value = def_value[def_value.find('{')+1:def_value.find('}')]
                    para['default'] = []
                    for pair in def_value.split(','):
                        p = pair.split(':')
                        para['default'].append({'key' : int(p[0].strip()), 'value' : float(p[1].strip())})
                    para['type'] = {'name' : 'dict'}
                else:
                    para['default'] =  def_value
                    para['type'] = {'name' : type(m.defaults[p_name]).__name__}
            else:
                para['type'] = ''
            if p_name in IMG and not p_name in igp_index:
                img_group_parameters.append(para)
                igp_index.add(p_name)
            elif p_name in MOD:
                parameters.append(para)

with open(f_models, 'w') as f:
    json.dump(models, f)

with open(f_image_groups, 'w') as f:
    json.dump(img_group_parameters, f)
