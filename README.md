# Обработка и структурирование научных публикаций в области материаловедения

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/armatveeeva/scientific-articles-processor/actions/workflows/ci.yml/badge.svg)](https://github.com/armatveeeva/scientific-articles-processor/actions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![NLP](https://img.shields.io/badge/NLP-ChemDataExtractor-orange)](https://chemdataextractor.org/)
[![Keyword Extraction](https://img.shields.io/badge/Keywords-YAKE-blue)](https://github.com/LIAAD/yake)

Репозиторий содержит программную реализацию пайплайна автоматизированного извлечения химических сущностей, генерации ключевых слов и структурирования метаданных из массива научных публикаций.

## Описание предмеа тной области

Современные научные базы данных содержат огромные массивы неструктурированного текста. Данный пайплайн решает задачу преобразования сырых текстов научных статей в структурированный машиночитаемый формат.

Система реализует следующие ключевые функции:
- Автоматическое распознавание химических элементов, соединений и материалов с использованием специализированной библиотеки `ChemDataExtractor`.
- Извлечение наиболее релевантных терминов из полного текста статьи с применением статистического алгоритма `YAKE` (Yet Another Keyword Extractor), не требующего предварительного обучения модели.
- Классификация статей по заданным тематическим категориям (например, металлы, композитные материалы, нанотехнологии) на основе совпадения с эталонными словарями.
- Формирование единого стандартизированного JSON-формата для последующего импорта в базы данных или проведения аналитических исследований.

## Технологический стек

- **Язык программирования:** Python 3.11+
- **Извлечение химических сущностей:** `chemdataextractor>=2.0`
- **Генерация ключевых слов:** `yake>=0.4.8`
- **Обработка данных:** `json`, `re` (стандартные библиотеки Python)
- **Хранилище данных:** Локальные структурированные JSON-файлы

## Архитектура

Пайплайн обработки данных разделен на модульные слои для обеспечения тестируемости и поддерживаемости:

```mermaid
flowchart LR
    subgraph Input
        A[Исходные JSON-файлы со статьями]
        K[config: словари категорий]
    end
    subgraph Pipeline
        B[Extractors: чтение и парсинг]
        C1[ChemDataExtractor: химические сущности]
        C2[YAKE: ключевые слова]
        C3[Классификатор: категория по словарям]
        D[Pydantic: валидация и схема результата]
    end
    subgraph Output
        E[Loaders: структурированный JSON]
    end
    A --> B
    B --> C1 & C2
    K --> C3
    C2 --> C3
    C1 --> D
    C2 --> D
    C3 --> D
    D --> E
```

## Быстрый старт

```bash
git clone https://github.com/armatveeeva/scientific-articles-processor.git
cd scientific-articles-processor
poetry install
poetry run <ВАША_КОМАНДА_ЗАПУСКА> --input <путь/к/входным/JSON> --output <путь/к/результату>
```

### Через Docker

```bash
docker build -t scientific-articles-processor .
docker run --rm -v "$(pwd)/data:/app/data" scientific-articles-processor <ВАША_КОМАНДА>
```

### Проверка кода и тесты

```bash
poetry run ruff check . && poetry run ruff format --check .
poetry run pytest
```
