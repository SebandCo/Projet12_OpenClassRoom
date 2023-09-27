def user_creation(request):
    surname = request.form.get("surname")
    name = request.form.get("name")
    department = request.form.get("department")

    print(surname)
    print(name)
    print(department)

    user = {"surname": surname,
            "name": name,
            "department": department}

    return user
