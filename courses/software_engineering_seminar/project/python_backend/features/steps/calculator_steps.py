from behave import step, given, when, then

try:
    from src import Calculator
    from src.models import Inp
except Exception as e:
    print(f"Error.{ e}")

@given("I have a Calculator")
def step_given_calulator(context):
    context.calculator = Calculator()
    context.first_number = None
    context.second_number = None
    context.operation = None
    context.result = None

@given("I have the first number {number: d}")
def step_given_first_number(context, number):
    context.first_number = number

@given("I have the second number {number: d}")
def step_given_second_number(context, number):
    context.second_number = number

@when("I perform {operation}")
def set_when_perform_operations(context, operation):
    calc_operation = operation if operation=="division" else "sum"

    if calc_operation == "sum":
        context.result = context.calculator.sum(context.first_number, context.second_number)
    elif calc_operation == "division":
        context.result = context.calculator.division(context.first_number, context.second_number)

@then("the result should be {expected_value:d}")
def step_then_result_int(context, expected_value):
    assert context.result is not None, "Empty result."
    assert context.result == expected_value 

@then("the result should be {expected_value:f}")
def step_then_result_float(context, expected_value):
    assert context.result is not None, "Empty result."
    assert abs(context.result - expected_value) < 0.0001 