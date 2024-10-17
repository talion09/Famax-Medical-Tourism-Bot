from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from tgbot.config import load_config

config = load_config(".env")


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            database=config.db.database,
            max_inactive_connection_lifetime=3
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):

        async with self.pool.acquire() as connection:
            connection: Connection()
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Famax_users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        number BIGINT NOT NULL,
        language VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    @staticmethod
    def format_args2(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=2)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id, number, language):
        sql = "INSERT INTO Famax_users (full_name, username, telegram_id, number, language) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, username, telegram_id, number, language, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Famax_users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Famax_users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_user(self, telegram_id, **kwargs):
        sql = "UPDATE Famax_users SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, *parameters, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Famax_users", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Famax_Admins (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE, 
        name VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_administrator(self, telegram_id, name):
        sql = "INSERT INTO Famax_Admins (telegram_id, name) VALUES ($1, $2) returning *"
        return await self.execute(sql, telegram_id, name, fetchrow=True)

    async def select_all_admins(self):
        sql = "SELECT * FROM Famax_Admins"
        return await self.execute(sql, fetch=True)

    async def select_id_admins(self):
        sql = "SELECT telegram_id FROM Famax_Admins"
        return await self.execute(sql, fetch=True)

    async def select_admin(self, **kwargs):
        sql = "SELECT * FROM Famax_Admins WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_admin(self, telegram_id):
        await self.execute("DELETE FROM Famax_Admins WHERE telegram_id=$1", telegram_id, execute=True)

    async def drop_admins(self):
        await self.execute("DROP TABLE Famax_Admins", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_doctors(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Doctors (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        specialist VARCHAR(255) NOT NULL,
        uz_specialist VARCHAR(255) NOT NULL,
        photo_id VARCHAR(255) NOT NULL,
        ru_text TEXT NOT NULL,
        uz_text TEXT NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_doctor(self, full_name, specialist, uz_specialist, photo_id, ru_text, uz_text):
        sql = "INSERT INTO Doctors (full_name, specialist, uz_specialist, photo_id, ru_text, uz_text) VALUES ($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, full_name, specialist, uz_specialist, photo_id, ru_text, uz_text, fetchrow=True)

    async def update_doctor(self, full_name, **kwargs):
        sql = "UPDATE Doctors SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE full_name=$1"
        return await self.execute(sql, full_name, *parameters, execute=True)

    async def select_all_doctors(self):
        sql = "SELECT * FROM Doctors"
        return await self.execute(sql, fetch=True)

    async def select_id_doctors(self):
        sql = "SELECT telegram_id FROM Doctors"
        return await self.execute(sql, fetch=True)

    async def select_doctor(self, **kwargs):
        sql = "SELECT * FROM Doctors WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_doctor(self, full_name):
        await self.execute("DELETE FROM Doctors WHERE full_name=$1", full_name, execute=True)

    async def drop_doctors(self):
        await self.execute("DROP TABLE Doctors", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_groups(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Famax_groups (
        id SERIAL PRIMARY KEY,
        group_id BIGINT NOT NULL UNIQUE, 
        group_name VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_group(self, group_id, group_name):
        sql = "INSERT INTO Famax_groups (group_id, group_name) VALUES ($1, $2) returning *"
        return await self.execute(sql, group_id, group_name, fetchrow=True)

    async def select_all_groups(self):
        sql = "SELECT * FROM Famax_groups"
        return await self.execute(sql, fetch=True)

    async def select_group(self, **kwargs):
        sql = "SELECT * FROM Famax_groups WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_group(self, group_id):
        await self.execute("DELETE FROM Famax_groups WHERE telegram_id=$1", group_id, execute=True)

    async def drop_groups(self):
        await self.execute("DROP TABLE Famax_groups", execute=True)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def create_table_about(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Famax_about (
        id SERIAL PRIMARY KEY,
        about_id INT NOT NULL UNIQUE, 
        photo_id TEXT NOT NULL,
        photo_id_uz TEXT NOT NULL,
        about TEXT NOT NULL,
        about_uz TEXT NOT NULL,
        contacts TEXT NOT NULL,
        contacts_uz TEXT NOT NULL
        );
        """
        await self.execute(sql, fetch=True)

    async def add_about(self, about_id, photo_id, photo_id_uz, about, about_uz, contacts, contacts_uz):
        sql = "INSERT INTO Famax_about (about_id, photo_id, photo_id_uz, about, about_uz, contacts, contacts_uz) " \
              "VALUES ($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, about_id, photo_id, photo_id_uz, about, about_uz, contacts, contacts_uz, fetchrow=True)

    async def update_about(self, about_id, **kwargs):
        sql = "UPDATE Famax_about SET "
        sql, parameters = self.format_args2(sql, parameters=kwargs)
        sql += f"WHERE about_id=$1"
        return await self.execute(sql, about_id, *parameters, execute=True)

    async def select_about(self, **kwargs):
        sql = "SELECT * FROM Famax_about WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_about(self, group_id):
        await self.execute("DELETE FROM Famax_about WHERE about_id=$1", group_id, execute=True)

    async def drop_about(self):
        await self.execute("DROP TABLE Famax_about", execute=True)


