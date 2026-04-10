import os
import glob

for filepath in glob.glob('/Users/mac/PycharmProjects/Chatbot/pages/*.py'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'print(' in content:
        content = content.replace('print(', 'logger.error(')
        
        if 'from utils.logger import get_logger' not in content:
            # inject logic
            lines = content.split('\n')
            last_import_index = 0
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    last_import_index = i
            
            lines.insert(last_import_index + 1, 'from utils.logger import get_logger\nlogger = get_logger(__name__)')
            content = '\n'.join(lines)
            
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Refactored {os.path.basename(filepath)}")
