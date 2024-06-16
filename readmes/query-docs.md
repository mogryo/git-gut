# Query documentation
## Basic form of a query
```bash
SHOW column-name-1,... column-name-N
FROM path-to-repo
WHERE column-name sign literal and/or ... 
ORDERBY column-name ASC/DESC ...
```
## Where statement
Where statement is parsed using Python AST module <br/>
[Official docs](https://docs.python.org/3/library/ast.html) <br/>
[Playground](https://astexplorer.net/) - Choose Python