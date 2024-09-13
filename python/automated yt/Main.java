// Define a class called Car
class Car {
    // Fields (attributes)
    String color;
    String model;
    int year;

    // Constructor to initialize the fields
    public Car(String color, String model, int year) {
        this.color = color;
        this.model = model;
        this.year = year;
    }

    // Method (behavior)
    void drive() {
        System.out.println("The car is driving.");
    }

    // Method to display car details
    void displayDetails() {
        System.out.println("Car Model: " + model + ", Color: " + color + ", Year: " + year);
    }
}

public class Main {
    public static void main(String[] args) {
        // Create an object of the Car class
        Car myCar = new Car("Red", "Toyota", 2022);
        
        // Call the methods of the object
        myCar.drive();  // Output: The car is driving.
        myCar.displayDetails();  // Output: Car Model: Toyota, Color: Red, Year: 2022
        
        // Create another object of the Car class
        Car anotherCar = new Car("Blue", "Honda", 2021);
        
        // Call the methods of the object
        anotherCar.drive();  // Output: The car is driving.
        anotherCar.displayDetails();  // Output: Car Model: Honda, Color: Blue, Year: 2021
    }
}
