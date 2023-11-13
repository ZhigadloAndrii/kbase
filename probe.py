from owlready2 import *

# Створюємо онтологію
ont = get_ontology("http://example.org/AutoKnowledgeBase")
owlready2.JAVA_EXE = "C:\\Program Files\\Common Files\\Oracle\\Java\\javapath\\java.exe"
with ont:

    class Car(Thing): pass
    class make(Car >> str, DataProperty): pass
    class model(Car >> str, DataProperty): pass
    class year(Car >> int, DataProperty): pass
    class speed(Car >> int, DataProperty): pass  # Додали новий клас для швидкості

    class Sedan(Car): pass
    class SUV(Car): pass
    class Coupe(Car): pass

    class Manufacturer(Thing): pass
    class produces(Manufacturer >> Car, ObjectProperty): pass

    class SportCar(Car): pass


    AllDisjoint([Sedan, SUV, Coupe])

    class hasColor(Car >> str, DataProperty): pass
    class hasEngineType(Car >> str, DataProperty): pass

    class isOlderThan(ObjectProperty, TransitiveProperty):
        domain = [Car]
        range = [Car]

    class isFasterThan(ObjectProperty, TransitiveProperty):
        domain = [Car]
        range = [Car]


    class isFastest(Car >> bool, DataProperty): pass

    class isSportCar(Car): pass


    r_faster = Imp();
    r_faster.set_as_rule("""Car(?c1), speed(?c1, ?s1), Car(?c2), speed(?c2, ?s2), greaterThan(?s1, ?s2) -> isFasterThan(?c1, ?c2)""")

    r_older = Imp(); r_older.set_as_rule("""Car(?c1), year(?c1, ?y1), Car(?c2), year(?c2, ?y2), lessThan(?y1, ?y2) -> isOlderThan(?c1, ?c2)""")

    r_sport_car = Imp();
    r_sport_car.set_as_rule("""Car(?c), isFasterThan(?c, ?otherCar), hasEngineType(?c, ?et), equal(?et, "V8") -> isSportCar(?c)""")

    ont.save("auto_ont.rtf")

    # Створюємо екземпляри автомобілів та виробників
    car1 = Car("Car1")
    car1.make = ["Toyota"]
    car1.model = ["Camry"]
    car1.year = [2020]
    car1.speed = [220]  # Додали швидкість
    car1.hasColor = ["Blue"]
    car1.hasEngineType = ["V6"]

    car2 = Car("Car2")
    car2.make = ["Honda"]
    car2.model = ["CR-V"]
    car2.year = [2019]
    car2.speed = [180]  # Додали швидкість
    car2.hasColor = ["Red"]
    car2.hasEngineType = ["4-cylinder"]

    car3 = Car("Car3")
    car3.make = ["Ford"]
    car3.model = ["Mustang"]
    car3.year = [2022]
    car3.speed = [300]  # Додали швидкість
    car3.hasColor = ["Black"]
    car3.hasEngineType = ["V8"]

    car4 = Car("Car4")
    car4.make = ["Chevrolet"]
    car4.model = ["Camaro"]
    car4.year = [2021]
    car4.speed = [250]  # Додали швидкість
    car4.hasColor = ["Yellow"]
    car4.hasEngineType = ["V6"]

    manufacturer1 = Manufacturer("Manufacturer1")
    manufacturer1.produces = [car1, car2, car3, car4]

    # Виконуємо логічний висновок
    pellet = sync_reasoner_pellet(infer_property_values=True)
    print("=== Виконання логічного висновку ===")
    print()

    # Виведення результатів тестів
    print("Car1 is older than:", car1.isOlderThan)
    print("Car1 is faster than:", car1.isFasterThan)

    print("Car2 is older than:", car2.isOlderThan)
    print("Car2 is faster than:", car2.isFasterThan)

    print("Car3 is older than:", car3.isOlderThan)
    print("Car3 is faster than:", car3.isFasterThan)

    print("Car4 is older than:", car4.isOlderThan)
    print("Car4 is faster than:", car4.isFasterThan)

    print("Car1 is a Sport Car:", isinstance(car1, isSportCar))
    print("Car2 is a Sport Car:", isinstance(car2, isSportCar))
    print("Car3 is a Sport Car:", isinstance(car3, isSportCar))
    print("Car4 is a Sport Car:", isinstance(car4, isSportCar))

