import re



class Table:
    def __init__(self, body: str) -> None:
        self.body = body

    def __str__(self) -> str:
        return self.get_name()

    def get_name(self) -> str:
        """
        Get name of table

        Returns:
            str: name of table
        """
        try:
            name = re.search(r"CREATE TABLE `.*?`", self.body, re.S).group()
            name = name.replace("CREATE TABLE ", "").replace("`", "")
            return name
        except:
            return None

    def get_primary_key(self) -> str | list[str]:
        """
        Return name (or list of names) of column(s) that might be a primary key 

        Returns:
            str | list[str]: primary key(s) column(s) name(s)
        """
        try:
            primary_keys = re.search(r"PRIMARY KEY \(`.*?`\)", self.body).group()
            primary_keys = primary_keys.replace("PRIMARY KEY (", "").replace(")", "").replace("`", "")
            if "," in primary_keys:
                return primary_keys.split(",")   # multiple primary keys
            else:
                return primary_keys     # one primary key
        except:
            return None

    def get_fields(self) -> list[str]:
        """
        Get names of all cols in a table

        Returns:
            list[str]: names of columns
        """
        fields = re.findall(r"`.*?`", self.body[self.body.index("("):])
        fields = [k.replace("`", "") for k in fields]
        return list(set(fields))

    def get_foreign_keys(self) -> list[str]:
        """
        Find cols that might be foreign keys (name is usually _____Id)

        Returns:
            list[str]: list containing names of cols that might be foreign keys
        """
        keys = list(filter(lambda x: x.endswith("Id"), self.get_fields()))
        keys = [k for k in keys if k != self.get_primary_key()]
        return keys

    def get_converted_body(self, other_tables: dict[str, str]) -> str:
        """
        Return query creating table with extra commands creating foreign keys 
        and changing DB engine to InnoDB (previously MyISAM)

        Args:
            other_tables (dict[str, str]): dict created with other tables, format is primary_key: table_name

        Returns:
            str: query creating a table (with foreign keys constraints)
        """
        temp = self.body.replace("ENGINE=MyISAM", "ENGINE=InnoDB")
        footer_template = "\n) ENGINE"     # 'regex' to detect end of creation query
        foreign_keys = self.get_foreign_keys()

        if not foreign_keys:
            return temp
        else:
            foreign_section = ""
            for key in foreign_keys:
                foreign_section += f",\nFOREIGN KEY ({key}) REFERENCES {other_tables[key]}({key})"

            temp = temp.replace(footer_template, foreign_section + footer_template)
            return temp

    def get_alters(self, other_tables: dict[str, str]) -> list[str]:
        """
        Get list of commands creating creating foreign keys for the table

        Args:
            other_tables (dict[str, str]): dict created with other tables, format is primary_key: table_name

        Returns:
            str: list of commands creating creating foreign keys for the table
        """
        foreign_keys = self.get_foreign_keys()

        if not foreign_keys:
            return []
        else:
            result = []
            name = self.get_name()
            for key in foreign_keys:               
                temp = f"ALTER TABLE {name} ADD FOREIGN KEY ({key}) REFERENCES {other_tables[key]}({key});"
                result.append(temp)
            return result


    def get_data(self):
        return {
            "body": self.body,
            "name": self.get_name(),
            "primary_key": self.get_primary_key(),
            "fields": self.get_fields(),
            "foreign_keys": self.get_foreign_keys(),
        }



if __name__ == "__main__":
    db_file = [k for k in open("f1db.sql")]
    sql = "".join(db_file)

    # converted_sql = sql.replace("ENGINE=MyISAM", "ENGINE=InnoDB")
    table_bodies = re.findall(r"CREATE TABLE.*?;", sql, re.S)
    tables = [Table(k) for k in table_bodies]

    db_tables = {table.get_name(): table for table in tables}
    foreign_keys = {table.get_primary_key(): table.get_name() for table in tables if isinstance(table.get_primary_key(), str)}


    new_sql = sql
    new_sql = new_sql.replace("ENGINE=MyISAM", "ENGINE=InnoDB")
    alters = []
    for t in db_tables:
        temp = db_tables[t].get_alters(foreign_keys)
        alters.extend(temp)

    new_sql += "\n"*3 + "\n".join(alters)
        # new_body = db_tables[t].get_converted_body(foreign_keys)
        # new_sql = new_sql.replace(db_tables[t].body, new_body)

    



    with open("new_db.sql", "w") as file:
        file.write(new_sql)
