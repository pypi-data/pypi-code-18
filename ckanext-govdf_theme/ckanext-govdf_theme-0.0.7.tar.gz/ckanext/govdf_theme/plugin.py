# encoding: utf-8
import routes.mapper
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base

def most_popular_groups():
    '''Retorna uma lista dos grupos com mais conjuntos de dados.'''

    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'package_count desc', 'all_fields': True})

    # Truncate the list to the 10 most popular groups only.
    groups = groups[:10]

    return groups


class Govdf_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.ITemplateHelpers)


    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'govdf_theme')

    def before_map(self, route_map):
        with routes.mapper.SubMapper(route_map, controller='ckanext.govdf_theme.plugin:Govdf_ThemeController') as m:

            m.connect('perguntas', '/perguntas', action='asks')
            m.connect('outros_dados', '/outros-dados', action='data_sugestions')
            m.connect('contato', '/contato', action='contact')
            m.connect('dados_abertos', '/dados-abertos', action='what_is_op')
            m.connect('mapa', '/mapa', action='map')
        return route_map

    def after_map(self, route_map):
        return route_map

    def get_helpers(self):
    	'''Registra a função most_popular_groups() como função helper do template'''
    	return {'govdf_theme_most_popular_groups': most_popular_groups}

class Govdf_ThemeController(base.BaseController):
    # Aqui são descritas as actions
    def asks(self):
        return base.render('content/perguntas.html')

    def data_sugestions(self):
        return base.render('content/outros-dados.html')

    def contact(self):
        return base.render('content/contato.html')

    def what_is_op(self):
        return base.render('content/dados-abertos.html')

    def map(self):
        return base.render('content/mapa.html')