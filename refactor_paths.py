import os
import re

# Mapping of old path string references to new module paths
REPLACEMENTS = {
    'web.app': 'fios_core.app',
    'web.gold_intelligence': 'gold_intelligence',
    '01_src/web': '01_src/fios_core',
}

def update_file_references(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.yaml', '.vbs', '.md', '.js', '.json')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    updated = content
                    for old_ref, new_ref in REPLACEMENTS.items():
                        updated = updated.replace(old_ref, new_ref)
                    
                    if updated != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(updated)
                        print(f'[+] Updated references in: {filepath}')
                except Exception as e:
                    print(f'[-] Error processing {filepath}: {e}')

if __name__ == '__main__':
    print('Updating internal code references...')
    update_file_references('01_src')
    update_file_references('04_tests')
    update_file_references('.')
