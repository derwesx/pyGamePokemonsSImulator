# Как играть в симулятор покемонов?

## Установка

Используйте менеджер пакетов [pip](https://pip.pypa.io/en/stable/) для установки pygame.

```bash
pip/pip3 install pygame
```
## Запуск
Для запуска игры необходимо запустить файл controller.py.
```
python3 controller.py
```
## Управление

```
S - Помочь противнику, отсортировав его колоду.
G - Помочь противнику, отдав ему своего лучшего покемона.
```
## Правила

### Порядок игры:
#### Игра проходит в 2 этапа: фарм покемонов, и их сражение. Изначально у каждого игрока нету покемонов, а на карте появляются покемоны. После того как все покемоны на карте будут пойманы, начинается этап битвы. Покемоны сражаются друг с другом, получая бонусы исходя из типов. Обратите внимание, что у покемонов есть шанс его поимки, который увеличивается от количества неудачных попыток поимки.

### Всего в игре существуют 4 типа покемонов:
#### Электрический - В момент атаки покемона водяного типа игнорирует всю броню.
#### Земляной - Имеет максимальную броню среди всех других покемонов
#### Водяной - Размягчает землю, понижая уровень брони. Тушит огонь, нанося больше урона
#### Огненный - Поджигает землю, нанося дополнительный урон.
#### У каждого из покемонов написана его статистика в формате Урон / Защита.
