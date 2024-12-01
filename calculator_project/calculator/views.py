import csv
from django.shortcuts import render
from django.conf import settings
import os

# Create your views here.




def save_to_csv(num1, num2, operation, result, ip_address):
    # Define the file path
    file_path = os.path.join(settings.BASE_DIR, "calculations.csv")
    
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # Open the file in append mode
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        # If the file is new, write the header
        if not file_exists:
            writer.writerow(["Number 1", "Number 2", "Operation", "Result", "IP Address"])
        # Write the data
        writer.writerow([num1, num2, operation, result, ip_address])







def home(request):
    if request.method == "POST":
        num1 = request.POST.get("num1")
        num2 = request.POST.get("num2")
        operation = request.POST.get("operation")
        result = None
        error = None

        try:
            # Convert inputs to floats for handling decimal values
            num1 = float(num1)
            num2 = float(num2)

            # Perform the operation
            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                if num2 != 0:
                    result = num1 / num2
                else:
                    error = "Cannot divide by zero."
            else:
                error = "Invalid operation."

            # Save the calculation if no error occurred
            if error is None:
                ip_address = get_client_ip(request)
                save_to_csv(num1, num2, operation, result, ip_address)

        except ValueError:
            error = "Please enter valid numbers."

        return render(request, "calculator/home.html", {"result": result, "error": error})

    return render(request, "calculator/home.html")



#Helper function to get the client's IP address.

def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip