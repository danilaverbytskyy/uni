# Cleaning Recommender (Flask + OWL)

Мини-приложение на Flask, которое подбирает пакеты услуг уборки на основе вашей онтологии из Protégé (OWL).

## Запуск

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Открыть: http://127.0.0.1:5000

## Где данные
`data/cleaning.owl` — ваша база знаний (OWL). Приложение читает:
- ZoneList (список зон)
- Zoning (связывает ZoneList → TaskList)
- TaskList (пакеты услуг) и их состав через `includes`
- Planning (если есть связь `defines` → TaskList), показывает Schedule и Resource pack

## Настройка под свою онтологию
Если в Protégé вы добавите новые экземпляры (TaskList/Tasks/Zoning и т.д.) — просто перезапишите файл `data/cleaning.owl`.
