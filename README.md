# Квест-мастер: Генератор приключений

## Описание проекта
Приложение для автоматизации создания квестов в Гильдии Приключенцев. Позволяет генерировать документы (свитки, контракты), рисовать карты локаций и вести учет выполненной работы с элементами геймификации.

https://private-user-images.githubusercontent.com/182104095/521183714-dfb5b866-5425-45d1-8bed-1ccfd1aa0ada.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjQ2NjAzOTgsIm5iZiI6MTc2NDY2MDA5OCwicGF0aCI6Ii8xODIxMDQwOTUvNTIxMTgzNzE0LWRmYjViODY2LTU0MjUtNDVkMS04YmVkLTFjY2ZkMWFhMGFkYS5tcDQ_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMjAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTIwMlQwNzIxMzhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1lZWNhNDM4MGE0M2Y2NWZhM2RkNWNkMWRlNTgwNmFhMDgzM2QxZjM5NzJhNmYxZDQxOWU2ZjVhNDMwMjUzYjIyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.W7ZipbOSOUu4OLGtcJFqlfz1_BEG8ohLQ0tE31Zwus8

## Функциональность
1.  **Мастер квестов**:
    *   Создание квестов с валидацией данных.
    *   Автосохранение в базу данных SQLite.
    *   Экспорт в PDF (WeasyPrint) и DOCX.
    *   Подсчет слов в описании (минимум 50 слов).
2.  **Редактор карт**:
    *   Рисование путей кистью.
    *   Размещение маркеров локаций (город, логово, таверна).
    *   Сохранение карты в изображение.
3.  **Геймификация**:
    *   Система уровней (Ученик -> Мастер -> Архимаг).
    *   Начисление XP за действия (создание квеста, экспорт, карта).

## Установка и запуск

1.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
    *Примечание: Для экспорта в PDF требуется библиотека WeasyPrint и GTK runtime.*

2.  Запустите приложение:
    ```bash
    python -m quest_master.main
    ```

## Структура проекта
*   `quest_master/` - Исходный код приложения.
    *   `gui/` - Графический интерфейс (PyQt6).
    *   `core/` - Логика (БД, шаблонизатор, геймификация).
    *   `templates/` - HTML-шаблоны для документов.
*   `parchments/` - Папка для сохраненных документов.
*   `tests/` - Тесты производительности.

## Технологии
*   Python 3.10+
*   PyQt6
*   Jinja2
*   SQLite
*   WeasyPrint
*   python-docx

