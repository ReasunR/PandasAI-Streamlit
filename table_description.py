from pandasai.connectors import PostgreSQLConnector

fields_info_employees = {'name': 'the name of employee, who is working in the company, table name: "employees"',
                         'department': 'from which department the employee is working',
                         'employee_id': 'the unique identifier of the employee',
                         'salary': 'how much the employee is earning, the income of the employee',
                         'title': 'the job title, the position of the employee in the company'}
table_description_employees = "This table contains information about name, department, employee_id, salary and title the employees in the company"

fields_info_informations = {'employee_id': 'the unique identifier of the employee, table name: "informations"',
                            'hobby': 'what employee likes to do in their free time',
                            'gender': 'Male or Female',
                            'zipcode': 'where the employee lives, the postal code of the employee', }
table_description_informations = "This table contains the hobby, zipcode and gender of the employees in the company"

employees_postgres = PostgreSQLConnector(
    config={
        "host": "localhost",
        "port": 5432,
        "database": "postgres",
        "username": "checkito950",
        "password": "123456",
        "table": "employees",
    },
    field_descriptions=fields_info_employees,
    description=table_description_employees,
)

informations_postgres = PostgreSQLConnector(
    config={
        "host": "localhost",
        "port": 5432,
        "database": "postgres",
        "username": "checkito950",
        "password": "123456",
        "table": "informations", },
    field_descriptions=fields_info_informations,
    description=table_description_informations
)