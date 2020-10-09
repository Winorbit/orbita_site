

О разнице между Client() and RequestsApi()

46

If you look at the tools and helpers for testing "standard" views in Django you will find something very analogue, the TestClient and a RequestFactory.

    The RequestFactory shares the same API as the test client. However, instead of behaving like a browser, the RequestFactory provides a way to generate a request instance that can be used as the first argument to any view. This means you can test a view function the same way as you would test any other function – as a black box, with exactly known inputs, testing for specific outputs.

The TestClient lets you interact with your site from the perspective of a user browsing your site (... though testing Javascript is yet another story). Many things come into play when testing your site like this (Sessions, Middlewares, URL-Routing, etc.). So these are typically more integrational tests that mimic real world interaction with your site or API.

A RequestFactory allows you to test you views in a very isolated manner. You can build a request and test your view without the need to setup your urls or care about things happening in middlewares etc. So this is closer to a typical unit test.

That said, both types of tests are useful. To get a general feeling if your API works as expected I would probably start using the APIClient and use RequestFactories when it comes to more complex views. But the right mix depends a lot on your concrete application.



- Упростить подключение настроек для разных энвов
- Добавить к БД таймауты
- таймауты для реквестов?
- Что вынести в энв-файлы?
- чек-лист для развертывания на проде
- юнит-тесты - что тестировать и как? Как запускать тесты? make?
- Настройки почты
- Pipfile в корне - он нужен или нужен отдельный пипфайл на каждый сервис?
- ЭНВФАЙЛЫ для разных энвов
- Где хранть энвы?
- healthcheck
- Есть проблема с классами при логировании
- Переделать поиск юзера - сейчас у меня 2 запроса в БД
- Авторизация - как правильно хранить, как передвать в реквете пароль - лучше в хэдере, мб?


 - SUPERUSER - FALSE, проверь дефолтные данные юзеров при создании, в т.ч дефолная группа
 - Вынессти настройки логгера в корень
