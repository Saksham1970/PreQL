import mysql.connector

class User():
    """ Creates an instance of User connection to Mysql Database.
    
    :param str host: Host or ip of database
    :param str user: Username
    :param str passwd: Password

    """
    
    def __init__(self,host,user,passwd):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.mydb = mysql.connector.connect(host = host,user=user,passwd=passwd)
        self.mycursor = self.mydb.cursor()
        
    def create_db(self,db_name):
        """ Creates a new database in the User connection.
    
        :param str db_name: Name of the database
        :return: The created Database
        :rtype: Database
        
        """

        self.mycursor.execute(f"CREATE DATABASE {db_name}")
        self.mydb.commit()
        return Database(self,db_name)
    
    def remove_db(self,db_name):
        """ Deletes a database in the User connection.
    
        :param str db_name: Name of the database
        
        """

        self.mycursor.execute(f"DROP DATABASE {db_name}")
        self.mydb.commit()

    @property
    def databases(self):
        """ Returns a tuple of all the database names in the User connection."""

        self.mycursor.execute(f"Show databases")
        databases = tuple()
        for x in self.mycursor:
            databases += x 
        return databases

class Database():
    """ Creates an instance of a Mysql Database.
    
    :param User user: The User Connection this Database is a part of
    :param str database: The name of the database

    """

    def __init__(self,user:User,database):
        
        self.database_name = database
        self.mydb = mysql.connector.connect(host = user.host,user=user.user,passwd=user.passwd)
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(f"USE {database}")

    @property
    def tables(self):
        """ Returns a tuple of all the table names in the database."""
        self.mycursor.execute(f"Show tables")
        tables = tuple()
        for x in self.mycursor:
            tables += x
        return tables

    def create_table(self,table_name,**attributes):
        """ Creates a new table
    
        :param str table_name: Name of the table
        :param str attributes: attributes with there definition like name = "varchar(20) Primary Key", number = "int(10)"
        :returns: The table created
        :rtype: Table
        """
        mycursor = self.mycursor
        mydb = self.mydb

        table_type = ""
        for arg in attributes:
            table_type+= f"{arg} {attributes[arg]},"
        table_type = table_type[:-1]

        mycursor.execute(f"create table {table_name}({table_type})")
        mydb.commit()
        return Table(self,table_name)

    def clone_table(self,new_table_name,table_name,columns:tuple = None, conditions:tuple =None):
        """ Clones an existing table.
    
        :param str new_table: The name of the new table
        :param str table_name: The name of the table to be cloned
        :param tuple columns: Only specified columns will be copied eg- ("name","number")
        :param tuple conditions: Only specified rows will be copied where conditions are satisfied eg- ('name = "chad"',"number = 69")
        :returns: The table created
        :rtype: Table
        """
        
        command = f"create table {new_table_name} "
        if columns:
            command+= f'select {",".join(columns)} from {table_name} '
        else:
            command+= f"select * from {table_name} "
        if conditions:
            command+=f'where {" and ".join(conditions)} '
        self.mycursor.execute(command)
        self.mydb.commit()
        return Table(self,new_table_name)

    def remove_table(self,table_name):
        """ Deletes a table.
    
        :param str table_name: The name of the table to be deleted
        
        """
        self.mycursor.execute(f"DROP TABLE {table_name}")
        self.mydb.commit()

class Table():
    """ Creates an instance of a table of a Database.
    
    :param Database database: The Database this Table is a part of
    :param str table_name: The name of the Table

    """

    def __init__(self,database:Database,table_name):
        self.mycursor = database.mycursor
        self.mydb = database.mydb
        self.table_name = table_name 
    
    @property
    def data(self):
        """
        Returns the data of the table in form of tuples.

        :return: Attributes (tuple)  and Data (list of tuples)
        """
        mycursor = self.mycursor

        data_type = tuple()
        data = []
        mycursor.execute(f"SHOW COLUMNS FROM {self.table_name}")
        for x in mycursor:
            data_type += (x[0],)

        mycursor.execute(f"select * from {self.table_name}")
        for x in mycursor:
            data += [x]

        return data_type,data

    def update(self,updates:tuple,conditions:tuple = None):
        """ Updates the table.
    
        :param tuple updates: The attributes to be update eg- ("marks = marks+10","number = 69")
        :param tuple conditions: Those rows will be updated where conditions are satisfied eg- ('name = "chad"',"number > 69")

        """

        command = f'UPDATE {self.table_name} set {",".join(updates)} '
        if conditions:
            command += f'where {",".join(conditions)}'
        self.mycursor.execute(command)
        self.mydb.commit()

    def select(self,columns:tuple = None, conditions:tuple =None):
        """ Selects/returns the data of the whole table or certain attributes and rows.
    
        :param tuple columns: Only specified columns will be selected eg- ("name","number")
        :param tuple conditions: Only specified rows will be selected where conditions are satisfied eg- ('name = "chad"',"number = 69")
        
        :return: Attributes (tuple)  and Data (list of tuples)
        """
        mycursor = self.mycursor
        data_type = tuple()
        data = []

        if not columns:
            mycursor.execute(f"SHOW COLUMNS FROM {self.table_name}")
            for x in mycursor:
                data_type += (x[0],)
        else:
            data_type = columns    
        command = f"select "
        if columns:
            command+= f'{",".join(columns)} from {self.table_name} '
        else:
            command+= f"* from {self.table_name} "
        if conditions:
            command+=f'where {" and ".join(conditions)} '
        mycursor.execute(command)

        for x in mycursor:
            data += [x]

        return data_type,data
      
    def search_exists(self,*conditions):
        """Searches if there is any entry which satisfies the conditions
    
        :param str conditions: conditions to be searched for eg- 'name = "chad"',"number = 69"
        :returns: Found(true) or not(false)
        :rtype: bool
        """

        mycursor = self.mycursor

        mycursor.execute(f'select * from {self.table_name} where {" And ".join(conditions)}')
        if len(list(mycursor)) == 0:
            return False
        else:
            return True

    def insert(self,**data):
        """ Inserts rows into the table
    
        :param str data: attributes with there values like name = "chad", number = "69"
       
        """

        mycursor = self.mycursor
        mydb = self.mydb

        keys = list(data.keys())
        values = list(data.values())

        for i in range(len(values)):
            if type(values[i]) == str:
                values[i] = '"' + values[i] + '"'
            else:
                values[i] = str(values[i])
            keys[i] = str(keys[i])

        values = ",".join(values)
        keys = ",".join(keys)

        mycursor.execute(f'insert into {self.table_name} ({keys}) values ({values})')
        mydb.commit()

    def delete(self,*conditions):
        """ Deletes rows into the table or delete all rows. If conditions are passed then only rows which satisfy are deleted else all rows are deleted.
    
        :param str conditions: rows only deleted if conditions satisfied  for eg- 'name = "chad"',"number = 69"
        """
        mycursor = self.mycursor
        mydb = self.mydb
        if conditions:
            mycursor.execute(f'delete from {self.table_name} where {" And ".join(conditions)}')
        else:
            mycursor.execute(f'delete from {self.table_name}')
        mydb.commit()
    
    def add_column(self,**columns):
        """
        Adds new columns to the table.

        :param str columns: new columns added, column name = type default value (if any) eg- mobile number = "int(10)", state = "varchar(10) default delhi"

        """
        table_type = ""
        for arg in columns:
            table_type+= f"{arg} {columns[arg]},"
        table_type = table_type[:-1]

        self.mycursor.execute(f"alter table {self.table_name} add({table_type})")
        self.mydb.commit()

    def rename_column(self,old_name,new_name):
        """
        Renames a column

        :param str old_name: The name of the column whose name needs to be changed
        :param str new_name: The new name

        """
        self.mycursor.execute(f"alter table {self.table_name} rename column {old_name} to {new_name}")
        self.mydb.commit()

    def remove_column(self,column_name):
        """
        Removes a column

        :param str column_name: The name of the column which needs to be removed

        """

        self.mycursor.execute(f"alter table {self.table_name} drop column {column_name}")
        self.mydb.commit()
    
    def print_table(self):
        """Print the Table in a Table-like manner"""
        
        data_type,data = self.data
        lengths = []
        for i in data_type:
            lengths+= [len(i)]
        for row in data:
            for j in range(len(row)):
                if len(str(row[j])) > lengths[j]:
                    lengths[j] = len(row[j])

        for i in range(len(data_type)):
            print(f'%-{lengths[i]}s' % (data_type[i]),end = "\t")
        print()        
        print()

        for row in data:
            for i in range(len(row)):
                print(f'%-{lengths[i]}s' % (row[i]),end = "\t")
            print()        