from calculator import Calc

# object instance
calculator = Calc()

MENU = """
Por favor, digite el número correspondiente a alguna de las 
siguientes opciones:
1. Sumar
2. Restar
3. Multiplicar
4. Dividir
5. Salir\n\n
"""

while True:
    print(MENU)
    option = int( input() )

    if option == 1: # sumar
        num1 = int( input("Ingrese el primer número de la suma:") )
        num2 = int( input("Ingrese el segundo número de la suma:") )
        print(f"El resultado de la suma es: { calculator.sum(num1, num2)} ")
    elif option == 2: # restar
        num1 = int( input("Ingrese el primer número de la resta: ") )
        num2 = int( input("Ingrese el segundo número de la resta: ") )
        print(f"El resultado de la resta es: { calculator.substract(num1, num2) }")
    elif option == 3: # multiplicar
        num1 = int( input("Ingrese el primer número de la multiplicación: ") )
        num2 = int( input("Ingrese el segundo número de la multiplicaciónL ") )
        print(f"El resultado de la multiplicación es: { calculator.multiplication(num1, num2) }")
    elif option == 4: # division
        enumerator = int( input("Ingrese el numerador de la división: ") )
        denominator = int( input("Ingrese el denominador de la división: ") )
        print(f"El resultado de la división es: { calculator.division(enumerator, denominator) }")
    elif option == 5: # salida
        break
    else:
        print("Por favor, seleccione una opción valida.")
