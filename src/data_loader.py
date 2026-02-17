import json
import os
from chemdataextractor import Document
import yake

def get_paths(directory_path):
    all_paths = []
    for item in os.scandir(directory_path):
        if item.is_dir():
            for i in os.listdir(item):
                file_path = os.path.join(item.path, i)
                all_paths.append(file_path)
        else:
            all_paths.append(item.path)
    return all_paths

def read_material_authors(authors_obj):
    authors = []
    for article_authors in authors_obj:
        author = {
            'name': article_authors.get('name'),
            'h-index': article_authors.get('h-index'),
            'scopus_id': article_authors.get('scopus_id'),
            'affiliations': [{
                'name': None,
                'country': None,
                'year_start': None,
                'year_end': None
            }]
        }
        authors.append(author)
    return authors

def read_materials(directory_path):
    articles = {}
    for file_path in get_paths(directory_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                obj = json.load(file)
                doc = Document(obj['text']['raw'])
                kw_extractor = yake.KeywordExtractor()
                keywords = kw_extractor.extract_keywords(obj['text']['raw'])
                sorted_keywords = sorted(keywords, key=lambda x: x[1])
                sorted_keywords = [item for item in sorted_keywords if 'Fig' not in item[0]]
                text_keywords = [item[0] for item in sorted_keywords[:15]]
                
                eid = obj.get('scopus_eid', 'unknown')
                material = {
                    'title': obj.get('title', ''),
                    'abstract': obj.get('abstract', ''),
                    'keywords': obj.get('keywords', []),
                    'info': {
                        'year': obj.get('published_year'),
                        'journal': obj.get('journal', {}).get('name'),
                        'scopus_eid': eid,
                        'scopus_pii': obj.get('pii'),
                        'doi': obj.get('doi')
                    },
                    'affiliations': obj.get('affiliations', []),
                    'countries': obj.get('countries', []),
                    'authors': read_material_authors(obj.get('authors', [])),
                    'full_text': obj['text']['raw'],
                    'chemical_elements': list(set([str(item) for item in doc.cems])),
                    'text_keywords': text_keywords,
                    'acknowledgment': obj.get('acknowledgment', '')
                }
                articles[eid] = material
        except Exception as e:
            print(f"Ошибка обработки {file_path}: {e}")
    return articles

def read_sputnik_authors_and_countries(obj):
    authors = []
    countries = []
    for article_author in obj:
        author = {
            'name': article_author.get('name'),
            'h-index': None,
            'scopus_id': article_author.get('scopus_author_id'),
            'affiliations': []
        }
        for affiliation in article_author.get('affiliations', []):
            author['affiliations'].append({
                'name': affiliation.get('name'),
                'country': affiliation.get('country'),
                'year_start': affiliation.get('year_start'),
                'year_end': affiliation.get('year_end')
            })
        authors.append(author)
        for country in article_author.get('countries', []):
            countries.append(country)
    return authors, countries

def read_sputnik(directory_path):
    articles = {}
    for file_path in get_paths(directory_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                item = json.load(file)
                doc = Document(item.get('article_text_mine', ''))
                eid = item.get('eid', 'unknown')
                authors, countries = read_sputnik_authors_and_countries(
                    item.get('author_information_mine', [])
                )
                article = {
                    'title': item.get('title', ''),
                    'abstract': item.get('abstract', ''),
                    'keywords': item.get('keywords', []),
                    'info': {
                        'year': item.get('year-nav'),
                        'journal': None,
                        'scopus_eid': eid,
                        'scopus_pii': item.get('pii-unformatted'),
                        'doi': item.get('identifier')
                    },
                    'affiliations': None,
                    'countries': countries,
                    'authors': authors,
                    'full_text': item.get('article_text_mine', ''),
                    'chemical_elements': list(set([str(item) for item in doc.cems])),
                    'text_keywords': item.get('keywords_mine', []),
                    'acknowledgment': item.get('funding-agency', '')
                }
                articles[eid] = article
        except Exception as e:
            print(f"Ошибка обработки {file_path}: {e}")
    return articles

def save_articles_to_json(articles, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(articles, file, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    print("Обработка каталога 'materials'...")
    materials = read_materials('Данные (1 этап)/materials')
    print('Сохранение файла materials.json...')
    save_articles_to_json(materials, './materials_v2.json')
    print('Файл сохранён')
