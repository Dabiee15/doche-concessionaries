import os
import re
import hashlib

template_dir = 'templates'
css_file = 'static/css/inline.css'
css_rules = {}

style_pattern = re.compile(r'style="([^"]*)"')
class_pattern = re.compile(r'class="([^"]*)"')

for root, _, files in os.walk(template_dir):
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            def repl(match):
                style_content = match.group(1).strip()
                if not style_content:
                    return ''
                # generate hash
                h = hashlib.md5(style_content.encode('utf-8')).hexdigest()[:8]
                class_name = f'gen-style-{h}'
                css_rules[class_name] = style_content
                return f'data-gen-class="{class_name}"'
            
            new_content = style_pattern.sub(repl, content)
            
            # Now we have data-gen-class="...". We need to merge it into class="..." or create one.
            def merge_classes(match):
                tag_content = match.group(0)
                # find data-gen-class
                gen_match = re.search(r'data-gen-class="([^"]+)"', tag_content)
                if not gen_match:
                    return tag_content
                
                gen_class = gen_match.group(1)
                tag_content = tag_content.replace(gen_match.group(0), '')
                
                has_class = re.search(r'class="([^"]*)"', tag_content)
                if has_class:
                    existing = has_class.group(1)
                    tag_content = tag_content.replace(has_class.group(0), f'class="{existing} {gen_class}"')
                else:
                    tag_content = tag_content.replace('>', f' class="{gen_class}">')
                # clean up multiple spaces before >
                tag_content = tag_content.replace('  >', ' >')
                return tag_content

            tag_pattern = re.compile(r'<[^>]+>')
            new_content = tag_pattern.sub(merge_classes, new_content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

with open(css_file, 'w', encoding='utf-8') as f:
    for cls, style in css_rules.items():
        f.write(f'.{cls} {{ {style} }}\n')
        
print("Styles extracted successfully.")
