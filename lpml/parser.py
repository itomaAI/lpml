import re
from typing import List, Dict, Union, Optional


Attributes = Dict[str, str]
Element = Dict[str, Union[str, Attributes, List['Element']]]
LPMLTree = List[Union[str, Element]]


PATTERN_ELEMENT = r'(<([^/>\s\n]+)([^/>\n]*)?>([\s\S]*)</\2>|<([^/>\s\n]+)([^/>\n]*)?/>)'
PATTERN_ATTRIBUTES = r'(\S*?)="(.*?)"'


def parse(text: str, exclude: Optional[List[str]] = None) -> LPMLTree:
    """Parse LPML text.

    Args:
        text (str): The text to parse.
        exclude (List[str]): Content of the specified tags will not be parsed.

    Returns:
        LPMLTree: The parsed tree.
    """
    if exclude is None:
        exclude = []

    matcher_attributes = re.compile(PATTERN_ATTRIBUTES)
    matcher_element = re.compile(PATTERN_ELEMENT)

    def _extract_attributes(text):
        attributes = {k: v for k, v in matcher_attributes.findall(text)}
        return attributes

    def _extract_element(text):
        if text is None:
            return None, None, None

        text_split = matcher_element.split(text, maxsplit=1)

        # no more tags
        if len(text_split) == 1:
            return text_split[0], None, None

        left = text_split[0]
        right = text_split[7]

        if text_split[5] is not None:
            tag = text_split[5]
            attributes = _extract_attributes(text_split[6])
            content = None
        else:
            tag = text_split[2]
            attributes = _extract_attributes(text_split[3])
            content = text_split[4]

        element = {
            'tag': tag,
            'attributes': attributes,
            'content': content
        }

        return left, element, right

    def _extract_elements_recursive(text):
        elements = []

        while True:
            left, element, text = _extract_element(text)
            if left != '':
                # <tag> のみを許可するか？
                elements += [left]

            if element is None:
                break

            if not (element['tag'] in exclude or element['content'] is None):
                content = element['content']
                content = _extract_elements_recursive(content)
                element['content'] = content

            elements += [element]
        return elements

    return _extract_elements_recursive(text)


def _repr_tag(tag, content, **kwargs):
    if kwargs:
        attr = ' ' + ' '.join([f'{k}="{v}"' for k, v in kwargs.items()])
    else:
        attr = ''
    bra = f'<{tag}{attr}>'
    ket = f'</{tag}>'
    emp = f'<{tag}/>'
    if content is None:
        return emp
    return ''.join([bra, content, ket])


def deparse(tree: LPMLTree) -> str:
    """Deparse LPML tree.

    Args:
        tree (LPMLTree): The tree to deparse.

    Returns:
        str: The deparsed text.
    """
    if tree is None:
        return tree

    text = ''

    for element in tree:
        if isinstance(element, str):
            text += element
            continue
        element['content'] = deparse(element['content'])
        text += _repr_tag(
            element['tag'], element['content'], **element['attributes'])
    return text


def findall(tree: LPMLTree, tag: str) -> List[Element]:
    """Find all elements with the specified tag."

    Args:
        tree (LPMLTree): The tree to search.
        tag (str): The tag to search for.

    Returns:
        List[Element]: The list of elements with the specified tag.
    """
    if tree is None:
        return []

    result = []
    for element in tree:
        if not isinstance(element, dict):
            continue
        if element['tag'] == tag:
            result.append(element)
        result += findall(element['content'], tag)
    return result
