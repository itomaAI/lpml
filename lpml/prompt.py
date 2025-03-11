from .parser import parse
from .parser import deparse
from .parser import Element
from typing import List


RULE_LPML_STR = '''<rule name="root rule">
All messages must be formatted in XML format. XML element ::= <tag attribute="value">content</tag> or <tag/>.
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</rule>'''

TAG_TAG_STR = '''<tag name="tag">
This tag defines a tag. The content must follow the definition of the tag.
Attributes:
    - name : A tag name.
</tag>'''

TAG_RULE_STR = '''<tag name="rule">
This tag defines rules. The defined content is absolute.
Attributes:
    - name (optional) : A rule name.
    - role (optional) : A role that should follow the rules. Roles are "system" or "assistant".
Notes:
    - The assistant must not use this tag.
</tag>'''

TAG_THINKING_STR = '''<tag name="thinking">
This tag represents a thought process.
Attributes:
    - label (optional) : A label summarizing the contents.
Notes:
    - The thought process must be described step by step.
    - This tag can be used repeatedly for each thought content and thought step.
    - In thinking, implicit inference or leaps in logic are not permitted. Even seemingly obvious inferences must be explicitly stated.
    - In mathematical reasoning, transformations of equations must be carried out in as much detail as possible.
    - Abbreviations are not allowed under any circumstances.
</tag>'''

TAG_REFLECTION_STR = '''<tag name="reflection">
This tag describes reflections on other elements.
By reflecting on previous thoughts (thinking elements) from various perspectives, it is possible to identify mistakes and deepen the thought process.
Attributes:
    - target (optional) : The label of the target element.
    - label (optional) : A label summarizing the contents.
Notes:
    - One reflection should be made for each thought content and thought step.
    - Before proceeding with thoughts one after another, it is important to pause and reflect.
</tag>'''

TAG_CODE_STR = '''<tag name="code">
This tag represents a code block. 
Only executable code can be written inside this tag.
Attgributes:
    - language : A programming language.
    - label (optional) : A label summarizing the contents.
Notes:
    - The code must be executable.
    - The system executes the code and returns the result.
    - The system returns standard output and error output, so if you need to obtain the execution result, use print statements or similar methods to output it.
</tag>'''

TAG_EOS_STR = '''<tag name="eos">
This tag represents the end of a message.
</tag>'''


RULE_LPML = parse(RULE_LPML_STR)[0]
TAG_TAG = parse(TAG_TAG_STR)[0]
TAG_RULE = parse(TAG_RULE_STR)[0]
TAG_THINKING = parse(TAG_THINKING_STR)[0]
TAG_REFLECTION = parse(TAG_REFLECTION_STR)[0]
TAG_CODE = parse(TAG_CODE_STR)[0]
TAG_EOS = parse(TAG_EOS_STR)[0]
EOS = {'tag': 'eos', 'attributes': {}, 'content': None}


PROMPT_BASE = [
    RULE_LPML, '\n\n',
    TAG_TAG, '\n\n',
    TAG_RULE, '\n\n',
    TAG_THINKING, '\n\n',
    TAG_REFLECTION, '\n\n',
    TAG_EOS, '\n\n',
]
PROMPT_BASE_STR = deparse(PROMPT_BASE)


def generate_element(tag: str, content: str, **attributes) -> Element:
    return {
        'tag': tag,
        'attributes': attributes,
        'content': content
    }


def generate_prompt(elements: List[Element], base_prompt=True) -> str:
    prompt = []
    if base_prompt:
        prompt += PROMPT_BASE

    for element in elements:
        prompt.append(element)
        prompt.append('\n\n')
    
    prompt.append(EOS)
    return deparse(prompt)
