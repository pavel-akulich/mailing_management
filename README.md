# Проект: Сервис управления рассылками

**Russian** | [English](docs_eng/README.md)

## Описание проекта

Проект "Сервис управления рассылками" представляет собой веб-приложение, разработанное на языке программирования Python
с использованием Django framework.
Проект включает в себя функционал для создания, управления и отслеживания рассылок, а также блог для продвижения сервиса.

## Составляющие части проекта

Проект состоит из следующих компонентов:

1. **Приложение home:**
    - Содержит базовый шаблон и шаблон отображения домашней(главной) страницы
    - Содержит контроллер `HomeView` для отображения главной страницы
    - Содержит функцию `get_cached_clients` для кэширования клиентов на главной странице в файле `services.py`

2. **Приложение blog:**
   - Содержит модель блога `Blog`
   - Содержит CRUD-механизм для создания, редактирования, просмотра и удаления статей блога
   - Реализованы права доступа, чтобы действия по управлению статьями блога принадлежали группе `"content_manager"`

3. **Приложение newsletter:**
    - Содержит модели настроек `MailingSettings`, рассылки `Message`, логов `MailingLogs`
    - Содержит CRUD-механизм для создания, редактирования, просмотра и удаления рассылок
    - Содержит шаблон и контроллер для отображения списка логов
    - Содержит команду `send_message` для запуска рассылки из терминала
    - Содержит функцию `send_newsletter` для автоматической рассылки сообщений в файле `services.py`
    - Содержит валидатор в файле `validators.py` для проверки формы создания/редактирования рассылки 

4. **Приложение service_client:**
   - Содержит модель для клиентов сервиса `Client`
   - Содержит CRUD-механизм для создания, редактирования, просмотра и удаления клиентов

5. **Приложение users:**
   - Содержит модель для пользователя `User`
   - Содержит шаблоны и контроллеры для входа, регистрации, верификации пользователя 
   - Содержит шаблон и контроллер, предоставляющие собой интерфейс для аккаунта менеджера
   - Содержит контроллер генерации нового пароля `GenerateNewPasswordView`, контроллеры по блокировке пользователя `DisableUserView` и рассылок `DisableMessageView`
   
6. **Директория static:**
    - Содержит `css-стили`, `изображения`, `JS код` 

## Технологии
   - Проект разработан на языке программирования `Python` с использованием `Django framework`
   - Для работы с базой данных используется сторонняя библиотека `psycopg2-binary`
   - Для выполнения периодических задач(автоматической рассылки) используется `django-crontab`
   - Для реализации кэширования в проекте применяется резидентная система управления базами данных `Redis`
   - Для управления виртуальным окружением используется инструмент `poetry`
   - Фронтенд часть проекта написана при помощи `HTML`, `CSS-стилей`, `JavaScript` и фреймворка `Bootstrap`

## Как установить и запустить проект
   - Необходимо сделать `fork` репозитория
   - Установите все зависимости из файла `pyproject.toml`
   - Создайте БД и выполните миграции для базы данных `python3 manage.py migrate`
   - Настройте необходимые переменные окружения указанные в файле `.env.sample`
   - Запустите сервер `python3 manage.py runserver`

## Как использовать проект
   - Изначально необходимо зарегистрироваться либо авторизоваться через почту и пароль
   - Далее как обычному пользователю вам доступен функционал по просмотру клиентов сервиса, ваших рассылок и отчетов ваших рассылок
   - Как обычный пользователь вы можете редактировать, удалять ваши рассылки и смотреть отчет рассылок. Рассылки и отчеты других пользователей вам не доступны
   - Настройки рассылки предоставляются на выбор из имеющегося списка
   - Есть возможность просматривать статьи из блога
   - Для менеджера доступен инструментарий менеджера, а именно:
      - Может просматривать любые рассылки
      - Может просматривать список пользователей сервиса и список клиентов
      - Может блокировать пользователей сервиса
      - Может отключать рассылки
      - Не может редактировать рассылки
      - Не может управлять списком рассылок
      - Не может изменять рассылки и сообщения
   - Контент менеджер имеет полные права для работы с CRUD-механизмом блога.
   - [Инструкция с фотографиями](https://drive.google.com/drive/folders/1vxBrn6-L6hmDqpilBML8Oqkayf8_Oo8C)

## Примечания
   - Проект был разработан как учебное задание и может быть доработан и расширен для более широкого использования
   - Интерфейсы для изменения и создания сущностей реализовали с помощью `Django-форм`
   - Переменные окружения, необходимые для работы проекта можно посмотреть в файле `.env.sample`
   - Все необходимые зависимости находятся в файле `pyproject.toml`
