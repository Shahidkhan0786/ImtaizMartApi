import requests

def register_schema(schema_str, subject_name):
    headers = {
        'Content-Type': 'application/vnd.schemaregistry.v1+json'
    }

    data = {
        "schemaType": "PROTOBUF",
        "schema": schema_str
    }

    response = requests.post(f'http://localhost:8081/subjects/{subject_name}/versions', headers=headers, json=data)

    if response.status_code == 200:
        print(f'Schema for {subject_name} registered successfully.')
    else:
        print(f'Failed to register schema for {subject_name}:', response.text)

# Read schema files
with open('app/proto/product.proto', 'r') as file:
    product_schema = file.read()

with open('app/proto/user.proto', 'r') as file:
    user_schema = file.read()

# Register schemas
register_schema(product_schema, 'product-value')
register_schema(user_schema, 'user-value')
