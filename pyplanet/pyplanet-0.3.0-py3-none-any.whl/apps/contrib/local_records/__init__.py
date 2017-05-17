import asyncio

from pyplanet.apps.config import AppConfig
from pyplanet.apps.contrib.local_records.views import LocalRecordsListView, LocalRecordsWidget
from pyplanet.apps.core.maniaplanet.models import Player
from pyplanet.contrib.command import Command
from pyplanet.contrib.setting import Setting

from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals

from pyplanet.utils import times

from .models import LocalRecord


class LocalRecords(AppConfig):
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.current_records = []
		self.widget = None

		self.setting_chat_announce = Setting(
			'chat_announce', 'Minimum index for chat announce', Setting.CAT_BEHAVIOUR, type=int,
			description='Minimum record index needed for public new record/recordchange announcement (0 for disable).',
			default=50
		)

	async def on_start(self):
		# Register commands
		await self.instance.command_manager.register(Command(command='records', target=self.show_records_list))

		# Register signals
		self.instance.signal_manager.listen(mp_signals.map.map_begin, self.map_begin)
		self.instance.signal_manager.listen(tm_signals.finish, self.player_finish)
		self.instance.signal_manager.listen(mp_signals.player.player_connect, self.player_connect)

		await self.context.setting.register(self.setting_chat_announce)

		# Load initial data.
		await self.refresh_locals()
		await self.chat_current_record()

		self.widget = LocalRecordsWidget(self)
		await self.widget.display()

	async def refresh_locals(self):
		record_list = await LocalRecord.objects.execute(
			LocalRecord.select(LocalRecord, Player)
				.join(Player)
				.where(LocalRecord.map_id == self.instance.map_manager.current_map.get_id())
				.order_by(LocalRecord.score.asc())
		)
		self.current_records = list(record_list)

	async def show_records_list(self, player, data = None, **kwargs):
		"""
		Show record list view to player.

		:param player: Player instance.
		:param data: -
		:param kwargs: -
		:type player: pyplanet.apps.core.maniaplanet.models.Player
		:return: view instance or nothing when there are no records.
		"""
		if not len(self.current_records):
			message = '$i$f00There are currently no records on this map!'
			await self.instance.chat(message, player)
			return

		# TODO: Move logic to view class.
		index = 1
		view = LocalRecordsListView(self)
		view_data = []
		first_time = self.current_records[0].score
		for item in self.current_records:
			record_player = item.player
			record_time_difference = ''
			if index > 1:
				record_time_difference = '$f00 + ' + times.format_time((item.score - first_time))
			view_data.append({'index': index, 'player_nickname': record_player.nickname,
							  'record_time': times.format_time(item.score),
							  'record_time_difference': record_time_difference})
			index += 1
		view.objects_raw = view_data
		view.title = 'Local Records on {}'.format(self.instance.map_manager.current_map.name)
		await view.display(player=player.login)
		return view

	async def map_begin(self, map):
		await self.refresh_locals()
		await asyncio.gather(
			self.chat_current_record(),
			self.widget.display()
		)

	async def player_connect(self, player, is_spectator, source, signal):
		await self.widget.display(player=player)

	async def player_finish(self, player, race_time, lap_time, cps, flow, raw, **kwargs):
		chat_announce = await self.setting_chat_announce.get_value()
		current_records = [x for x in self.current_records if x.player_id == player.get_id()]
		score = lap_time

		previous_index = None
		previous_time = None

		if len(current_records) > 0:
			current_record = current_records[0]
			if score > current_record.score:
				# No improvement, ignore
				return

			# Temporary make index + time local for the messages.
			previous_index = self.current_records.index(current_record) + 1
			previous_time = current_record.score

			# If equal, only show message.
			if score == current_record.score:
				message = '$fff{}$z$s$0f3 equalled the $fff{}.$0f3 Local Record: $fff\uf017 {}$0f3.'.format(
					player.nickname, previous_index, times.format_time(score)
				)

				if chat_announce >= previous_index:
					return await self.instance.chat(message)
				elif chat_announce != 0:
					return await self.instance.chat(message, player.login)

		else:
			current_record = LocalRecord(
				map=self.instance.map_manager.current_map,
				player=player,
			)

		# Set details (score + cps times).
		current_record.score = score
		current_record.checkpoints = ','.join([str(cp) for cp in cps])

		# Add to list when it's a new record!
		if current_record.get_id() is None:
			self.current_records.append(current_record)

		# (Re)sort the record list.
		self.current_records.sort(key=lambda x: x.score)
		new_index = self.current_records.index(current_record) + 1

		# Prepare messages.
		if previous_index is not None:
			if new_index < previous_index:
				message = '$fff{}$z$s$0f3 gained the $fff{}.$0f3 Local Record: $fff\uf017 {}$0f3 ($fff{}.$0f3 $fff-{}$0f3).'.format(
					player.nickname, new_index, times.format_time(score), previous_index,
					times.format_time((previous_time - score))
				)
			else:
				message = '$fff{}$z$s$0f3 improved the $fff{}.$0f3 Local Record: $fff\uf017 {}$0f3 ($fff-{}$0f3).'.format(
					player.nickname, new_index, times.format_time(score),
					times.format_time((previous_time - score))
				)
		else:
			message = '$fff{}$z$s$0f3 drove the $fff{}.$0f3 Local Record: $fff\uf017 {}$0f3.'.format(
				player.nickname, new_index, times.format_time(score)
			)

		# Save to database (but don't wait for it).
		asyncio.ensure_future(current_record.save())

		coros = [self.widget.display()]
		if chat_announce >= new_index:
			coros.append(self.instance.chat(message))
		elif chat_announce != 0:
			coros.append(self.instance.chat(message, player))
		await asyncio.gather(*coros)

	async def chat_current_record(self):
		records_amount = len(self.current_records)
		if records_amount > 0:
			first_record = self.current_records[0]
			message = '$0f3Current Local Record: $fff\uf017 {}$z$s$0f3 by $fff{}$z$s$0f3 ($fff{}$0f3 records)'.format(
				times.format_time(first_record.score), first_record.player.nickname, records_amount
			)
			calls = list()
			calls.append(self.instance.chat(message))
			for player in self.instance.player_manager.online:
				calls.append(self.chat_personal_record(player))
			await self.instance.gbx.multicall(*calls)
		else:
			message = '$0f3There is no Local Record on this map yet.'
			await self.instance.chat(message)

	def chat_personal_record(self, player):
		record = [x for x in self.current_records if x.player_id == player.get_id()]

		if len(record) > 0:
			message = '$0f3You currently hold the $fff{}.$0f3 Local Record: $fff\uf017 {}'.format(
				self.current_records.index(record[0]) + 1, times.format_time(record[0].score)
			)
			return self.instance.chat(message, player)
		else:
			message = '$0f3You don\'t have a Local Record on this map yet.'
			return self.instance.chat(message, player)
