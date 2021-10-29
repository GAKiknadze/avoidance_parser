from aiosqlite import connect


class DB(object):
	GET_ONE = 'GET_ONE'
	GET_ALL = 'GET_ALL'
	SET_ONE = 'SET_ONE'
	SET_ALL = 'SET_ALL'

	@classmethod
	async def create(cls, name):
		self = DB()
		self.name = name
		self.base = await connect(name)
		return self

	def __check_vals(self, vals):
		msg = None, 'tuple'
		if isinstance(vals, tuple):
			msg = vals, 'tuple'
		elif isinstance(vals, list):
			msg = vals, 'list'
		return msg

	async def __execute(self, sql, vals, method=None):
		ans = None
		vals, v_type = self.__check_vals(vals)
		cursor = await self.base.cursor()
		funcs = {
			'list': cursor.executemany,
			'tuple': cursor.execute,
			self.GET_ONE: cursor.fetchone,
			self.GET_ALL: cursor.fetchall
		}
		await funcs[v_type](sql, vals)
		ans = await funcs[method]() if method else None
		await self.base.commit()
		await cursor.close()
		return ans

	async def get_param(self, param):
		SQL = 'SELECT val FROM config WHERE name = ?;'
		return await self.__execute(SQL, (param,), method=self.GET_ONE)

	async def set_all_items(self, param):
		SQL = 'INSERT OR IGNORE INTO all_items VALUES (?);'
		await self.__execute(SQL, param)

	async def get_all_items(self):
		SQL1 = 'SELECT * FROM all_items LIMIT 20;'
		SQL2 = 'DELETE FROM all_items WHERE id=?;'
		ans = await self.__execute(SQL1, (), self.GET_ALL)
		await self.__execute(SQL2, ans)
		return ans

	async def set_valid_items(self, param):
		SQL = 'INSERT OR IGNORE INTO valid_items VALUES (?,?);'
		await self.__execute(SQL, param)

	async def get_valid_items(self):
		SQL1 = 'SELECT * FROM valid_items LIMIT 5;'
		SQL2 = 'DELETE FROM valid_items WHERE url=?;'
		ans = await self.__execute(SQL1, (), self.GET_ALL)
		del_ans = [(i[0],) for i in ans]
		await self.__execute(SQL2, del_ans)
		return ans

	async def set_data(self, param):
		SQL = 'INSERT OR IGNORE INTO data VALUES (?,?,?,?,?,?,?,?);'
		await self.__execute(SQL, param)
