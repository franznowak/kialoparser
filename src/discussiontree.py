import re
from packaging import version


class DiscussionTree():
    def __init__(self, filename=None):
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        self.title = lines[0].split(":", 1)[1][1:]
        self.claims = lines[3:]
        self.tree = {}
        title_claim = lines[2]
        last_index = re.search(r"^(\d+.)+", title_claim).group()
        stance = None
        content = re.match(r"^(\d+.)+ *(.*)", title_claim).group(2)
        for claim in self.claims:
            if re.search(r"^(\d+.)+", claim) is None:
                continue
            index = re.search(r"^(\d+.)+", claim).group()
            # if debug:
            #     print(index, last_index)
            if index.startswith('1.') and version.parse(index) > version.parse(last_index):
                self.set_entry(last_index, {"index": last_index, "stance": stance, "content": content})
                last_index = index
                if re.search(r"(Con|Pro)(?::)|None", claim) is not None:
                    stance = re.search(r"(Con|Pro)(?::)|None", claim).group(1)
                    content = re.search(r"((Con|Pro)(?::\s))(.*)", claim).group(3)
                else:
                    stance = None
                    content = re.match(r"^(\d+.)+ *(.*)", claim).group(2)
            else:
                content += re.match(r"^(\d+.)+ *(.*)", claim).group(2)
        self.set_entry(index, {"index": index, "stance": stance, "content": content})

    def find(self, search_string: str):
        """ Finds claims that contain a certain string.
        
            params:
                search_string: (reg ex) string to search for.

            returns:
                list of indices that contain the string.
        """
        indices = []
        for claim in self.claims:
            if re.search(search_string, claim, re.IGNORECASE) is not None:
                index_re = re.search(r"^(\d+.)+", claim)
                if index_re is not None:
                    indices.append(index_re.group())

        return indices

    def find_list(self, search_string_list: list):
        """ Finds claims that contain one of a list of string.
        
            params:
                search_string_list: list of strings to search for.

            returns:
                list of indices that contain one of the strings.
        """
        indices = []
        for claim in self.claims:
            for search_string in search_string_list:
                index_re = re.search(r"^(\d+.)+", claim)
                if index_re is not None:
                    indices.append(index_re.group())

        return indices

    def get_title(self):
        return self.title

    def get_claims(self):
        return self.claims

    def get_entry(self, index):
        """ params:
                index: keyspec of the form "(d\.)+"

            returns:
                node at given index
        """
        return self._get_node(self._get_entry(index))

    def _get_node(self, subtree):
        return {"index": subtree["index"], "content": subtree["content"],
                "stance": subtree["stance"]} if "index" in subtree.keys() else {}

    def _get_entry(self, index):
        """ params:
                index: keyspec of the form "(d\.)+"

            returns:
                full subtree dict at given index
        """
        if index == '.':
            return self.tree

        keys = self._index_to_keys(index)

        result = self.tree[keys[0]]
        for key in keys[1:]:
            result = result[key]

        return result

    def set_entry(self, index, entry):
        """ params:
                index: keyspec of the form "(d\.)+"
                entry: dict at given index
        """
        keys = self._index_to_keys(index)
        level = self.tree
        for key in keys[:-1]:
            if key in level:
                level = level[key]
            else:
                level[key] = {}
                level = level[key]
        level[keys[-1]] = entry

    def get_parent(self, index):
        """ params:
                index: keyspec of the form "(d\.)+"

            returns:
                dict at parent of given index, or empty dict if index is root
        """
        parent_index = self._get_parent_index(index)
        if parent_index=='.':
            return None
        return self.get_entry(parent_index)

    def get_children(self, index):
        """ params:
                index: keyspec of the form "(d\.)+"

            returns:
                iterable of dicts that are children of given index, or empty dict if index is root
        """
        subtree = self._get_entry(index)
        result = []
        for key in subtree.keys():
            if key not in ["index", "content", "stance"]:
                result.append(self._get_node(subtree[key]))
        return result

    def get_siblings(self, index):
        """ params:
                index: keyspec of the form "(d\.)+"

            returns:
                iterable of dicts that are children of the parent of the given index
        """
        parent_index = self._get_parent_index(index)
        subtree = self._get_entry(parent_index)
        result = []
        for key in subtree.keys():
            if key not in ["index", "content", "stance"] and subtree[key]["index"] != index:
                result.append(self._get_node(subtree[key]))
        return result

    def _index_to_keys(self, index):
        return index.split('.')[:-1]

    def _get_parent_index(self, index):
        return '.'.join(self._index_to_keys(index)[:-1]) + '.'
