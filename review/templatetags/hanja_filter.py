from django import template
import re

register = template.Library()

@register.filter(name='hanja_style')
def hanja_style(text):
    hanja_pattern = re.compile(r'[\u4e00-\u9fff]')  # 한자의 유니코드 범위
    if hanja_pattern.search(text):
        return f'<span class="hanja-font">{text}</span>'
    return text




@register.filter(name='is_hanja')
def is_hanja(text):
    if text is None:
        return False
    
    hanja_pattern = re.compile(r'[\u4e00-\u9fff]')  # 한자의 유니코드 범위
    return bool(hanja_pattern.search(text))
