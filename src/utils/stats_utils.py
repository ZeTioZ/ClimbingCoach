import pickle

from database.queries import run_queries
from gui.app_state import AppState
from database.models.run import Run


def get_derivation_stat(app_state: AppState, selected_run: Run) -> float:
	current_route = app_state.get_route()
	current_route_holds = pickle.loads(current_route.holds)
	selected_run_hit_holds = pickle.loads(selected_run.holds)
	hit_run_holds_counter = 0

	for current_route_hold in current_route_holds:
		for selected_run_hit_hold in selected_run_hit_holds:
			if str(current_route_hold) == str(selected_run_hit_hold):
				hit_run_holds_counter += 1
				break
	return 100.00 - (int((hit_run_holds_counter / len(current_route_holds)) * 10000)/100)


def get_user_route_records(app_state: AppState):
	"""Return the user route records."""
	user = app_state.get_user()
	selected_route = app_state.get_route()
	user_route_records = run_queries.get_runs_by_user_and_route(user.username, selected_route.name)
	return user_route_records.sort(key=lambda x: x.runtime)


def get_all_users_route_records(app_state: AppState):
	"""Return all the route records."""
	selected_route = app_state.get_route()
	all_route_records = run_queries.get_runs_by_route(selected_route.name)
	return all_route_records.sort(key=lambda x: x.runtime)
