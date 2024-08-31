/**
 * This is a module used to define an example of an abstract class.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 * 
 * =============================================
 * LICENCE - FOSS [Free Open Software Source]
 */

/*
This class is a concrete example of the abstract class.
*/
public class ConcreteClass extends AbstractClass{
    
    public ConcreteClass(Object parameter){
        super(parameter);
    }

    @Override
    public void abstractMethod(){
        System.out.println("This is the implementation of the abstract method in the ConcreteClass");
    }

    public static void main(String[] args){
        ConcreteClass concreteClass = new ConcreteClass("This is the parameter for the ConcreteClass");
        concreteClass.abstractMethod();
    }
}