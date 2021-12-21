# Graph Colourizer
Алгоритм, що розмальовує кожну вершину неорієнтованого граф в один з трьох кольорів `(червоний, зелений, синій)`, крім того який був початковим для певної вершини.
Після виконання основної функції, повертається список пар `(номер вершини, новий колір)`.

**Автори:**
- Стрельбицький Кирило
- Краснянський Тимур
- Ніколайченко Іван
- Марків Олена
- Сітарчук Марія

## Запуск модуля
Для запуску модуля необхідно виконати
```console
$ python3 main.py -file /path_to_graph
```
Де `/path_to_graph` - шлях до **csv** файлу, що зберігає граф.

## Формат введення графу
Нехай в графі **n** вершин, тоді кожній вершині відповідає номер **v<sub>i</sub>** такий, що <code>1 ≤ v<sub>i</sub> ≤ n</code>.<br>Кольори задаються латинськими літерами `R, G, B`, які позначають червоний, зелений і синій кольори відповідно.<br>
Граф задається через **csv** файл, що має таку структуру колонок: 
1. перша вершина ребра
2. друга вершина ребра
3. колір першої вершини
4. колір другої вершини.

## Аналіз задачі
Кожна вершина графа має бути розфарбована в один з трьох кольорів. Розглянемо деяку вершину **a** і введемо булеві змінні <code>a<sub>r</sub>, a<sub>g</sub>, a<sub>b</sub></code>, тоді:
- якщо для a обрано червоний колір, то змінна <code>a<sub>r</sub> = true, a<sub>g</sub> = false, a<sub>b</sub> = false</code>.
- якщо для a обрано зелений колір, то змінна <code>a<sub>r</sub> = false, a<sub>g</sub> = true, a<sub>b</sub> = false</code>.
- якщо для a обрано синій колір, то змінна <code>a<sub>r</sub> = false, a<sub>g</sub> = false, a<sub>b</sub> = true</code>.

### Умови існування валідного розфарбування
1. Обмеження, що дві вершини, наприклад **a** і **b**, з'єднані ребром `(a, b)` не можуть бути одного кольори, можна записати так:
<code>(~a<sub>r</sub> ∨ ~b<sub>r</sub>) ∧ (~a<sub>g</sub> ∨ ~b<sub>g</sub>) ∧ (~a<sub>b</sub> ∨ ~b<sub>b</sub>)</code>.
2. Кожна вершина повинна бути пофарбовано в якийсь колір, отже
<code>(a<sub>r</sub> ∨ a<sub>g</sub> ∨ a<sub>b</sub>)</code>.
3. Кожна вершина має бути пофарбована лише в один колір
<code>(~a<sub>r</sub> ∨ ~a<sub>g</sub>) ∧ (~a<sub>g</sub> ∨ ~a<sub>b</sub>) ∧ (~a<sub>r</sub> ∨ ~a<sub>b</sub>)</code>.

Ми отримали умови для кожної **вершини** та **ребра**.

### Знаходження значень змінних
Для знаходження значень кожної з змінних, застосуємо принципи розв'язку 2-SAT задачі. Перепишем диз'юнкції у вигляді імплікацій застошувавши перетворення 
a∨b еквівалентно ~a⇒b ∧ ~b⇒a. Та побудуємо орієнтований граф імплікацій, в якому ребро (x1, x2) позначає імплікацію x1⇒x2. 
Умови 1 та 3 переписати в такий вигляд можливо, але умова 2 має вигляд виразу в формі 3-SAT. Задача 3-SAT є NP-повною, тож не може бути розв’язана за поліноміальний час. Отже нам треба звести умову до 2-SAT задачі, і для цього ми використаємо факт наданий в умові – кожна вершина не може бути пофарбована в початковий колір. 
Використання цього факту дає нам можливість виключити з  розгляду одну вершину, адже якщо цей колір використовувати не можна, її значення одразу є false і не впливатиме на рішення. Через ту саму причину, не будемо включати в граф імплікацій ребра, які є інцидентними до забороненої вершини. Отже ми отримаємо нові умови, де a1 і a2 позначають перший та другий дозволені кольори:
Умова 1. (~a1 ∨ ~b2) ∧ (~a1 ∨ ~b2).
Умова 2. (a1 ∨ a2)
Умова 3. (~a1 ∨ ~a2)

Побудувавши граф імплікацій, ми можемо використати розв'язок 2-SAT для знаходження значень кожної вершини графу імплікацій, які б задовольняли накладеним умовам. Тепер якщо значення ar = true і червоний не є заблокованим кольором для цієї вершини, то перефарбувати цю вершину потрібно в червоний. Так само перевіряємо інші кольори для всіх вершин графу.

