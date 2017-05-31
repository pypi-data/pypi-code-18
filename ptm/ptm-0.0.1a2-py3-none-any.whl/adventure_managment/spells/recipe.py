from re import match

Ingredient = namedtuple('Ingredient', [('synonyms', List[str]), 'type',
                        ('description', str), 'default', 'value'])


class Recipe:
    def __init__(self, *ingredients):
        if self._controll_ingredients(ingredients):
            self.ingredients = ingredients
        else:
            raise TypeError

    @staticmethod
    def _controll_ingredients(ingredients):
        ingredients_names = [*ingredient.synonyms for ingredient in ingredients]
        ingredients_names_count = map(
            lambda ingredient_name: ingredients_names.count(ingredient_name), ingredients_names)
        return True if list(filter(lambda ingredient_name_count: ingredient_name_count > 1,
                                   ingredients_names_count)) else False

    @staticmethod
    def _get_ingredients(ingredients):
        return {self._get_ingredient_name(Ingredient): ingredient for ingredient in ingredients}

    def __getattr__(self, attribute):
        return _get_ingredient(attribute).value

    def __setattr__(self, attribute, value):
        _get_ingredient(attribute).value = value

    def _get_ingredient(self, ingredient_name):
        target_ingreient = self._find_ingredient_value(attribute)
        if not target_ingreient:
            raise AttributeError
        return target_ingreient

    def _find_ingredient(self, ingredient_name):
        target_ingredients = set(
            filter(lambda ingredient: self._is_ingredient(ingredient_name, ingredient.synonyms),
                   self.ingredients))
        return target_ingredients and target_ingredients[0]

    def _is_ingredient(self, ingredient_name, synonyms):
        return ingredient_name == self._get_filtered_synonym(
                lambda synonym: not synonym.startswith('-'), synonyms) \
            or ingredient_name == self._get_filtered_synonym(
                lambda synonym: match(r'^--/w+', synonym), synonyms) \
            or ingredient_name == self._get_filtered_synonym(
                lambda synonym: match(r'^-/w+', synonym), synonyms)

    @staticmethod
    def _get_filtered_synonym(filter_function, synonyms):
        filtered_synonyms = filter(filter_function, synonyms)
        return filtered_synonyms[0].lstrip('-') if filtered_synonyms else None

    def set_ingredients_values(self, values):
        for ingredient_name, ingredient_value in values.items():
            setattr(self, ingredient_name, ingredient_value)

    def __iter__(self):
        return self.ingredients
