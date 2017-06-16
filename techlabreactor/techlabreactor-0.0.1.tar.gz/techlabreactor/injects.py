from sc2reader.events import *
from sc2reader.objects import Player
from sc2reader.resources import Replay

TIME_LIMIT_SECONDS = 60 * 7 * 1.4
QUEEN_INJECT_SECONDS = 40


def _hatchery_events_for_player(player: Player, replay: Replay) -> dict:
    time_limit = TIME_LIMIT_SECONDS * int(replay.game_fps)

    player_hatcheries = [
        x.unit
        for x
        in replay.tracker_events
        if (
            (isinstance(x, UnitInitEvent) or isinstance(x, UnitBornEvent)) and
            x.unit.name in ["Hatchery", "Lair", "Hive"] and
            x.unit.owner == player and
            (x.unit.finished_at is not None and x.unit.finished_at <= TIME_LIMIT_SECONDS * replay.game_fps)
        )]

    hatchery_events = dict(
        (hatchery, [
            (hatchery.finished_at if hatchery.finished_at else 0, "Start"),
            (min(hatchery.died_at if hatchery.died_at else time_limit, replay.frames, time_limit), "End")])
        for hatchery
        in player_hatcheries)

    spawn_larvae_events = [
        x
        for x
        in replay.game_events
        if (
            isinstance(x, CommandEvent) and
            x.ability_name == "SpawnLarva" and
            x.player == player and
            x.frame <= time_limit and
            x.target in player_hatcheries
        )]

    for spawn_larvae_event in spawn_larvae_events:
        hatchery_events[spawn_larvae_event.target].append((spawn_larvae_event.frame, "Inject"))

    for event_lists in hatchery_events.values():
        event_lists.sort(key=lambda x: x[0])

    return hatchery_events


def _events_to_inject_states(events: list, fps: int) -> dict:
    inject_stack = []
    state_changes = []

    for event_time, event_name in events:
        if event_name == "Start":
            state_changes.append((event_time, False))
        else:
            while inject_stack and inject_stack[0] <= event_time:
                inject_pop = inject_stack[0]
                inject_stack = inject_stack[1:]

                if not inject_stack:
                    state_changes.append((inject_pop, False))

            if event_name == "End":
                state_changes.append((event_time, state_changes[-1][1]))
            elif event_name == "Inject":
                inject_stack.append(event_time + QUEEN_INJECT_SECONDS * fps)

                if not state_changes[-1][1]:
                    state_changes.append((event_time, True))

    return state_changes


def get_hatchery_inject_states_for_player(player: Player, replay: Replay) -> list:
    hatchery_events = _hatchery_events_for_player(player, replay)

    hatchery_inject_state_changes = dict(
        (hatchery, _events_to_inject_states(events, int(replay.game_fps)))
        for hatchery, events
        in hatchery_events.items())

    return list(sorted(hatchery_inject_state_changes.values(), key=lambda x: x[0]))


def calculate_inject_efficiency(inject_states: list):
    injected_frames = 0
    not_injected_frames = 0

    for state_changes in inject_states:
        for i, state_change in enumerate(state_changes[1:]):
            was_injected = state_changes[i][1]
            is_injected = state_change[1]

            interval = state_change[0] - state_changes[i][0]

            if is_injected and was_injected:
                injected_frames += interval
            elif is_injected and not was_injected:
                not_injected_frames += interval
            elif not is_injected and was_injected:
                injected_frames += interval
            elif not is_injected and not was_injected:
                not_injected_frames += interval

    return injected_frames / (not_injected_frames + injected_frames)



