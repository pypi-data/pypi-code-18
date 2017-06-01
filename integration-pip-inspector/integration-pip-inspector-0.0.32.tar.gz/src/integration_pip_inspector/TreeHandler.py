from integration_pip_inspector.FileHandler import generate_file, FILE_NAME


class TreeHandler(object):
    tree = None

    def __init__(self, tree):
        self.tree = tree

    def render_tree(self,  output_path=None):
        result = self._render_tree_helper(self.tree)
        if output_path:
            generate_file(
                result, FILE_NAME, output_path)
        return result

    def _render_tree_helper(self, tree_node, layer=1):
        result = tree_node.name + "==" + tree_node.version
        dependencies = sorted(tree_node.dependencies, key=lambda x: x.name)
        for dependency in dependencies:
            result += "\n" + (" " * 4 * layer)
            result += self._render_tree_helper(dependency, layer + 1)
        return result
