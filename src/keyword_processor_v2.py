import os
import json

def load_data():
    with open('words.json', 'r', encoding='utf-8') as f:
        words = json.load(f)
    with open('materials.json', 'r', encoding='utf-8') as f:
        materials = json.load(f)
    with open('sputnik.json', 'r', encoding='utf-8') as f:
        sputnik = json.load(f)
    return words, materials, sputnik

def process_articles(words, materials, sputnik):
    for category, keywords in words.get('words', {}).items():
        if not os.path.exists(category):
            os.mkdir(category)
        
        for keyword in keywords:
            print(f'COLLECTING {category} - {keyword}...', end='\t')
            num = 0
            dir_path = os.path.join(category, keyword)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            
            # Обработка материалов
            for idx, material in enumerate(materials):
                elements = (
                    material.get('chemical_elements', []) +
                    material.get('keywords', []) +
                    material.get('text_keywords', [])
                )
                elements = [str(e).lower() for e in elements]
                if keyword.lower() in elements:
                    num += 1
                    with open(os.path.join(dir_path, f'{idx}.json'), 'w', encoding='utf-8') as f:
                        json.dump(material, f, ensure_ascii=False, indent=2)
            
            # Обработка sputnik
            offset = len(materials)
            for idx, item in enumerate(sputnik):
                elements = (
                    item.get('chemical_elements', []) +
                    item.get('keywords', []) +
                    item.get('text_keywords', [])
                )
                elements = [str(e).lower() for e in elements]
                if keyword.lower() in elements:
                    num += 1
                    with open(os.path.join(dir_path, f'{idx + offset}.json'), 'w', encoding='utf-8') as f:
                        json.dump(item, f, ensure_ascii=False, indent=2)
            
            print(f'Найдено: {num}')

if __name__ == '__main__':
    words, materials, sputnik = load_data()
    process_articles(words, materials, sputnik)
