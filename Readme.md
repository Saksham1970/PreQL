# PreQL

PreQL is a library for linking MySql database with python without knowing much about MySQL language.


## Getting Started

```py
from preql import User, Database, Table

root = User("localhost", "root", "root")
library = Database(root, "library")
books = Table(library, "books")

```

License
----

MIT
