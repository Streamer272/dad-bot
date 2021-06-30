# SS3DBC
Short for 'Smart SQLite3 Database Controller'. SS3DBC is a modern python package that uses SQLite3 to communicate with database.

## Usage
Database class instance creation:
```python
db = Database("/path/to/your/database.sql")
```
Database functions and properties:
- `location` - returns database location
- `tables` - returns list of all tables in database
- `get_table(name)` - returns table where name = "name"
- `create_table(name, query)` - creates table with name "name" and values "query"
- `delete_table(name)` - deletes table where name = "name"
- `query(query)` - returns query result
- `execute(query)` - executes query
